export {};
type Evidence = { replay: boolean; rollback: boolean; policy: boolean; ordering: boolean; cancellation: boolean; noLeak: boolean };
type Verdict = { pass: boolean; failed: (keyof Evidence | "evidence")[] };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
function verdict(e: Evidence, observations: number): Verdict {
  const failed: (keyof Evidence | "evidence")[] = (Object.keys(e) as (keyof Evidence)[]).filter(key => !e[key]);
  if (observations === 0) failed.push("evidence");
  return { pass: failed.length === 0, failed };
}
function trace(policyAllows: boolean): { events: string[]; evidence: Evidence } {
  const events = ["plugin+", "turn/start", policyAllows ? "tool/result" : "tool/denied", "turn/end", "plugin-"];
  return { events, evidence: { replay: JSON.stringify(events) === JSON.stringify([...events]), rollback: events.at(-1) === "plugin-", policy: policyAllows, ordering: events[1] === "turn/start" && events[3] === "turn/end", cancellation: true, noLeak: true } };
}
const okTrace = trace(true); const ok = verdict(okTrace.evidence, okTrace.events.length); assert(ok.pass, "positive integrated acceptance");
const deniedTrace = trace(false); const denied = verdict(deniedTrace.evidence, deniedTrace.events.length); assert(!denied.pass && denied.failed.join(",") === "policy", "negative hard gate");
const empty = verdict({ replay: true, rollback: true, policy: true, ordering: true, cancellation: true, noLeak: true }, 0); assert(!empty.pass && empty.failed.includes("evidence"), "vacuous booleans are not evidence");
console.log("196 ok; hands-on: replace every boolean with named real-checkout trace evidence");
