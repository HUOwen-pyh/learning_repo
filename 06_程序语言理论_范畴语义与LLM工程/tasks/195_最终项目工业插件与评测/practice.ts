export {};
type Trial = { taskId: string; taskScore: number; policyViolations: number; leaks: number; success: boolean };
type TaskStability = { taskId: string; trials: number; successes: number; estimate: number };
type Report = { accepted: boolean; meanTask: number; passK: number; byTask: TaskStability[] };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
function passHatEstimate(successes: number, trials: number, k: number): number {
  if (k === 0) return 1;
  if (successes < k) return 0;
  let ratio = 1;
  for (let i = 0; i < k; i++) ratio *= (successes - i) / (trials - i);
  return ratio;
}
function evaluate(trials: readonly Trial[], k: number): Report {
  assert(Number.isInteger(k) && k >= 0, "k must be a non-negative integer");
  const meanTask = trials.length ? trials.reduce((sum, row) => sum + row.taskScore, 0) / trials.length : 0;
  const groups = new Map<string, Trial[]>();
  for (const trial of trials) groups.set(trial.taskId, [...(groups.get(trial.taskId) ?? []), trial]);
  if (k > 0) for (const [taskId, rows] of groups) assert(rows.length >= k, `${taskId} must have at least k trials`);
  const byTask = [...groups].map(([taskId, rows]) => {
    const successes = rows.filter(row => row.success).length;
    return { taskId, trials: rows.length, successes, estimate: passHatEstimate(successes, rows.length, k) };
  });
  const passK = k === 0 ? 1 : (byTask.length ? byTask.reduce((sum, row) => sum + row.estimate, 0) / byTask.length : 0);
  return { accepted: trials.length > 0 && trials.every(row => row.policyViolations === 0 && row.leaks === 0), meanTask, passK, byTask };
}
const good = evaluate([{ taskId: "a", taskScore: 1, policyViolations: 0, leaks: 0, success: true }], 1); assert(good.accepted && good.passK === 1, "positive");
const mixed = evaluate([
  { taskId: "a", taskScore: 1, policyViolations: 0, leaks: 0, success: true }, { taskId: "a", taskScore: 1, policyViolations: 0, leaks: 0, success: true }, { taskId: "a", taskScore: 0, policyViolations: 0, leaks: 0, success: false },
  { taskId: "b", taskScore: 1, policyViolations: 0, leaks: 0, success: true }, { taskId: "b", taskScore: 1, policyViolations: 0, leaks: 0, success: true }, { taskId: "b", taskScore: 1, policyViolations: 0, leaks: 0, success: true },
], 2);
assert(Math.abs(mixed.passK - 2 / 3) < 1e-12, "pass^k averages C(c,k)/C(n,k), including n > k");
assert(Math.abs(mixed.byTask.find(row => row.taskId === "a")!.estimate - 1 / 3) < 1e-12, "two successes among three give C(2,2)/C(3,2)");
let failed = false; try { evaluate([{ taskId: "short", taskScore: 1, policyViolations: 0, leaks: 0, success: true }], 2); } catch { failed = true; } assert(failed, "insufficient trials fail loud");
const unsafe = evaluate([{ taskId: "a", taskScore: 1, policyViolations: 1, leaks: 0, success: true }], 1); assert(!unsafe.accepted, "hard gate negative");
assert(!evaluate([], 1).accepted && evaluate([], 1).passK === 0, "empty positive-k report");
assert(evaluate([], 0).passK === 1, "empty product gives pass^0=1");
console.log("195 ok; hands-on: compare empirical task-wise pass^k with the real plugin trial report");
