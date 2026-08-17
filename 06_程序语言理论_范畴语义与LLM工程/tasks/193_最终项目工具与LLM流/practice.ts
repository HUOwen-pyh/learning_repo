export {};
type Chunk = { seq: number; kind: "text" | "tool"; data: string };
type Tool = { valid(x: unknown): boolean; run(x: unknown): string };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
function assemble(chunks: readonly Chunk[]): { text: string; calls: string[] } {
  chunks.forEach((c, i) => assert(c.seq === i, "non-contiguous chunks"));
  return { text: chunks.filter(c => c.kind === "text").map(c => c.data).join(""), calls: chunks.filter(c => c.kind === "tool").map(c => c.data) };
}
function invoke(tool: Tool, raw: string): string { let args: unknown; try { args = raw ? JSON.parse(raw) : {}; } catch { args = raw; } assert(tool.valid(args), "invalid tool arguments"); return tool.run(args); }
const message = assemble([{ seq: 0, kind: "text", data: "Hi" }, { seq: 1, kind: "tool", data: "{\"x\":2}" }]);
assert(message.text === "Hi" && message.calls.length === 1, "positive assembly");
const double: Tool = { valid: x => typeof x === "object" && x !== null && typeof (x as { x?: unknown }).x === "number", run: x => String((x as { x: number }).x * 2) };
assert(invoke(double, message.calls[0]) === "4", "tool result");
let failed = false; try { assemble([{ seq: 1, kind: "text", data: "x" }]); } catch { failed = true; } assert(failed, "negative order");
assert(assemble([]).text === "", "boundary empty stream");
console.log("193 ok; hands-on: retain raw chunks plus one immutable completion anchor");
