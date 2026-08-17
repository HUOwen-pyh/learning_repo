type Tool = { name: string; valid: (x: unknown) => boolean; execute: (x: unknown) => unknown; render: (x: unknown) => string };
type Result = { canonical: unknown; content: string };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

class Tools {
  private map = new Map<string, Tool>(); private observers: Array<(name: string, result: Result) => void> = [];
  register(tool: Tool): () => void { assert(!this.map.has(tool.name), "duplicate tool"); this.map.set(tool.name, tool); return () => { this.map.delete(tool.name); }; }
  onResult(fn: (name: string, result: Result) => void): void { this.observers.push(fn); }
  call(name: string, args: unknown): Result {
    const tool = this.map.get(name); assert(tool, "unknown tool"); assert(tool.valid(args), "invalid args");
    const canonical = tool.execute(args); const result = { canonical, content: tool.render(canonical) };
    this.observers.forEach(fn => fn(name, result)); return result;
  }
}

const tools = new Tools(); const events: string[] = []; tools.onResult((name, r) => events.push(name + ":" + r.content));
const dispose = tools.register({ name: "greet", valid: x => typeof x === "string", execute: x => "Hello, " + x, render: String });
assert(tools.call("greet", "Cordis").canonical === "Hello, Cordis", "positive"); assert(events[0] === "greet:Hello, Cordis", "event");
let failed = false; try { tools.call("greet", 1); } catch { failed = true; } assert(failed, "negative args");
dispose(); failed = false; try { tools.call("greet", "x"); } catch { failed = true; } assert(failed, "boundary disposed registration");
console.log("175 ok; hands-on: attach a policy guard before execute and trace every rejection");
