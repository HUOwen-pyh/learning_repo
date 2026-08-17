export {};
type WireDelta = Readonly<{ reasoning?: string; text?: string; tool?: { index: number; id?: string; name?: string; args: string } }>;
type CourseStreamChunk =
  | Readonly<{ type: "reasoning-delta" | "text-delta"; index: number; text: string }>
  | Readonly<{ type: "tool-call-delta"; index: number; id: string; name?: string; argumentsDelta: string }>
  | Readonly<{ type: "usage"; input: number; output: number }>
  | Readonly<{ type: "finish"; reason: "stop" | "tool-calls" }>;
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
function translate(wire: readonly WireDelta[], usage: { input: number; output: number }, reason: "stop" | "tool-calls"): CourseStreamChunk[] {
  const out: CourseStreamChunk[] = [];
  for (const delta of wire) {
    if (delta.reasoning) out.push({ type: "reasoning-delta", index: 0, text: delta.reasoning });
    if (delta.text) out.push({ type: "text-delta", index: 1, text: delta.text });
    if (delta.tool) out.push({ type: "tool-call-delta", index: delta.tool.index + 2, id: delta.tool.id ?? "", ...(delta.tool.name === undefined ? {} : { name: delta.tool.name }), argumentsDelta: delta.tool.args });
  }
  out.push({ type: "usage", ...usage }, { type: "finish", reason });
  return out;
}
function assemble(chunks: readonly CourseStreamChunk[]): { reasoning: string; text: string; toolArgs: string; terminal: string } {
  const positions = new Map<number, string>(); let terminal = "";
  chunks.forEach((chunk, index) => {
    if (chunk.type === "finish") { assert(index === chunks.length - 1, "nothing may follow finish"); terminal = chunk.reason; return; }
    if (chunk.type === "usage") { assert(chunks[index + 1]?.type === "finish", "usage must precede finish"); return; }
    const fragment = chunk.type === "tool-call-delta" ? chunk.argumentsDelta : chunk.text;
    positions.set(chunk.index, (positions.get(chunk.index) ?? "") + fragment);
  });
  return { reasoning: positions.get(0) ?? "", text: positions.get(1) ?? "", toolArgs: positions.get(2) ?? "", terminal };
}
function renderPrompt(template: string, values: Readonly<Record<string, string | undefined>>): string {
  return template.replace(/\{\{([a-z][a-z0-9_]*)\}\}/g, (_all, name: string) => { const value = values[name]; assert(value !== undefined, `unknown variable: ${name}`); return value; });
}
const chunks = translate([{ reasoning: "think" }, { text: "Hi" }, { tool: { index: 0, id: "c1", name: "lookup", args: "{\"x\":" } }, { tool: { index: 0, args: "2}" } }], { input: 3, output: 4 }, "tool-calls");
const message = assemble(chunks);
assert(message.reasoning === "think" && message.text === "Hi" && message.toolArgs === "{\"x\":2}", "wire fragments assemble by block index");
assert(chunks.at(-2)?.type === "usage" && chunks.at(-1)?.type === "finish", "provider defers usage and finish");
assert(renderPrompt("Hello {{name}}", { name: "Ada" }) === "Hello Ada", "prompt render preflight");
let failed = false; try { renderPrompt("{{missing}}", {}); } catch { failed = true; } assert(failed, "unknown variable fails loud");
console.log("188 ok; hands-on: compare these chunks with DeepSeek translate and BlockAssembler specs");
