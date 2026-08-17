interface ServiceMap {
  clock: { now(): number };
  upper: { apply(text: string): string };
}
type FactoryMap<T> = { [K in keyof T]: () => T[K] };
type Return<F> = F extends (...args: never[]) => infer R ? R : never;

function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

class Registry<T extends object> {
  private readonly factories: Partial<FactoryMap<T>>;
  constructor(factories: Partial<FactoryMap<T>>) { this.factories = factories; }
  get<K extends keyof T>(key: K): T[K] {
    const factory = this.factories[key];
    if (!factory) throw new Error("missing service: " + String(key));
    return factory();
  }
}

const registry = new Registry<ServiceMap>({
  clock: () => ({ now: () => 7 }),
  upper: () => ({ apply: text => text.toUpperCase() }),
});
assert(registry.get("clock").now() === 7, "positive");
assert(registry.get("upper").apply("") === "", "boundary");
let failed = false;
try { new Registry<ServiceMap>({}).get("clock"); } catch { failed = true; }
assert(failed, "negative missing runtime registration");
const typeOnly: Return<() => number> = 1;
assert(typeOnly === 1, "conditional infer");
console.log("167 ok; hands-on: augment ServiceMap with logger and register it");
