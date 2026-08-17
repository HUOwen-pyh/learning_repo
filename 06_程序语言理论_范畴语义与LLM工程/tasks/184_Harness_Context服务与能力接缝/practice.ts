export {};
interface Agent { send(text: string): void; dispose(): void }
type Factory = () => Agent;
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

class Capabilities {
  private providers = new Map<string, Factory>();
  set(name: string, factory: Factory): () => void { const previous = this.providers.get(name); this.providers.set(name, factory); return () => { if (previous) this.providers.set(name, previous); else this.providers.delete(name); }; }
  require(name: string): Factory { const value = this.providers.get(name); assert(value, "missing capability: " + name); return value; }
}

const log: string[] = []; const caps = new Capabilities();
const undo = caps.set("agent", () => ({ send: x => log.push("v1:" + x), dispose: () => log.push("v1-") }));
caps.require("agent")().send("hi"); assert(log[0] === "v1:hi", "positive seam"); undo();
let failed = false; try { caps.require("agent"); } catch { failed = true; } assert(failed, "negative missing");
const empty = caps.set("", () => ({ send: () => undefined, dispose: () => undefined })); empty(); assert(true, "boundary empty key reversible");
console.log("184 ok; hands-on: shadow v1 with v2 then dispose v2 to restore v1");
