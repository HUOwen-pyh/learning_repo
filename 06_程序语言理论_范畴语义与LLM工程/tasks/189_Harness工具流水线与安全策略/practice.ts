export {};
type Call = { id: number; name: string; allowed: boolean; run: () => string };
type Result = { id: number; ok: boolean; text: string };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function execute(calls: readonly Call[], abortedAt = Infinity): Result[] {
  return calls.map((c, index) => {
    if (index >= abortedAt) return { id: c.id, ok: false, text: "ABORTED_BEFORE_DISPATCH" };
    if (!c.allowed) return { id: c.id, ok: false, text: "DENIED" };
    try { return { id: c.id, ok: true, text: c.run() }; } catch (e) { return { id: c.id, ok: false, text: e instanceof Error ? e.message : "error" }; }
  });
}

const results = execute([{ id: 2, name: "slow", allowed: true, run: () => "a" }, { id: 1, name: "denied", allowed: false, run: () => "x" }]);
assert(results.map(x => x.id).join(",") === "2,1" && results[1].text === "DENIED", "positive model order and policy");
assert(execute([{ id: 0, name: "boom", allowed: true, run: () => { throw new Error("BODY"); } }])[0].text === "BODY", "negative body");
assert(execute([], 0).length === 0, "boundary empty");
assert(execute([{ id: 9, name: "x", allowed: true, run: () => "x" }], 0)[0].text === "ABORTED_BEFORE_DISPATCH", "abort");
console.log("189 ok; hands-on: classify calls into exclusive barriers and bounded parallel groups");
