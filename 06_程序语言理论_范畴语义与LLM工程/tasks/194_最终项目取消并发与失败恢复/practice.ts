export {};
type Job = { id: string; mode: "parallel" | "exclusive"; outcome: "ok" | "transient" | "terminal" };
type Result = { id: string; status: "ok" | "retry" | "error" | "aborted" };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
function partition(jobs: readonly Job[]): Job[][] {
  const groups: Job[][] = []; let parallel: Job[] = [];
  const flush = (): void => { if (parallel.length) { groups.push(parallel); parallel = []; } };
  for (const job of jobs) {
    if (job.mode === "exclusive") { flush(); groups.push([job]); }
    else parallel.push(job);
  }
  flush(); return groups;
}
function schedule(jobs: readonly Job[], abortAt = Infinity): Result[] {
  return jobs.map((job, i) => {
    if (i >= abortAt) return { id: job.id, status: "aborted" };
    if (job.outcome === "ok") return { id: job.id, status: "ok" };
    if (job.outcome === "transient") return { id: job.id, status: "retry" };
    return { id: job.id, status: "error" };
  });
}
const out = schedule([{ id: "a", mode: "parallel", outcome: "ok" }, { id: "b", mode: "exclusive", outcome: "transient" }]);
assert(out.map(x => x.id).join("") === "ab" && out[1].status === "retry", "positive model order");
const groups = partition([
  { id: "a", mode: "parallel", outcome: "ok" }, { id: "b", mode: "parallel", outcome: "ok" },
  { id: "x", mode: "exclusive", outcome: "ok" }, { id: "c", mode: "parallel", outcome: "ok" },
]);
assert(groups.map(group => group.map(job => job.id).join("")).join("|") === "ab|x|c", "exclusive call forms a barrier");
assert(schedule([{ id: "x", mode: "parallel", outcome: "terminal" }])[0].status === "error", "negative terminal");
assert(schedule([{ id: "x", mode: "parallel", outcome: "ok" }], 0)[0].status === "aborted", "abort boundary");
assert(schedule([]).length === 0, "empty");
console.log("194 ok; hands-on: replace each parallel group with a bounded async executor and preserve commit order");
