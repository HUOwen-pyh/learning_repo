export {};
type Edge = { event: string; producer: string; consumer: string; mode: "notify" | "waterfall" };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function audit(declared: readonly string[], edges: readonly Edge[]): { orphaned: string[]; unhandled: string[] } {
  const produced = new Set(edges.map(e => e.event)); const consumed = new Set(edges.filter(e => e.consumer.length > 0).map(e => e.event));
  return { orphaned: declared.filter(e => !produced.has(e)), unhandled: [...produced].filter(e => !consumed.has(e)).sort() };
}

const report = audit(["turn/start", "agent/request", "ghost"], [
  { event: "turn/start", producer: "loop", consumer: "ui", mode: "notify" },
  { event: "agent/request", producer: "loop", consumer: "router", mode: "waterfall" },
]);
assert(report.orphaned[0] === "ghost" && report.unhandled.length === 0, "positive audit");
assert(audit([], []).orphaned.length === 0, "boundary empty graph");
assert(audit([], [{ event: "x", producer: "p", consumer: "", mode: "notify" }]).unhandled[0] === "x", "negative no consumer");
console.log("185 ok; hands-on: reject waterfall events with more than one terminal owner");
