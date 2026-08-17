interface Events { token: { text: string }; done: { usage: number } }
type Listener<T> = (payload: T) => void;
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

class Bus<E extends object> {
  private listeners = new Map<keyof E, Array<Listener<never>>>();
  on<K extends keyof E>(key: K, fn: Listener<E[K]>): () => void {
    const list = this.listeners.get(key) ?? [];
    list.push(fn as Listener<never>); this.listeners.set(key, list);
    return () => { const i = list.indexOf(fn as Listener<never>); if (i >= 0) list.splice(i, 1); };
  }
  emit<K extends keyof E>(key: K, payload: E[K]): void {
    for (const fn of this.listeners.get(key) ?? []) (fn as Listener<E[K]>)(payload);
  }
}

type Tool<A, R> = { valid: (x: unknown) => x is A; run: (x: A) => R };
const add: Tool<{ x: number; y: number }, number> = {
  valid: (x): x is { x: number; y: number } => typeof x === "object" && x !== null && typeof (x as { x?: unknown }).x === "number" && typeof (x as { y?: unknown }).y === "number",
  run: x => x.x + x.y,
};
function call<A, R>(tool: Tool<A, R>, raw: unknown): R { assert(tool.valid(raw), "invalid args"); return tool.run(raw); }

const bus = new Bus<Events>(); const seen: string[] = [];
const off = bus.on("token", x => seen.push(x.text)); bus.emit("token", { text: "a" }); off(); bus.emit("token", { text: "b" });
assert(seen.join("") === "a", "positive and unsubscribe boundary");
assert(call(add, { x: 2, y: 3 }) === 5, "tool positive");
let failed = false; try { call(add, { x: "2", y: 3 }); } catch { failed = true; } assert(failed, "negative validation");
console.log("168 ok; hands-on: add divide with a non-zero validator");
