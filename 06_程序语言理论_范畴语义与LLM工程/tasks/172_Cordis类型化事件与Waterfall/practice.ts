interface Events { normalize: string; observed: { name: string } }
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

class Waterfall<E extends object> {
  private handlers = new Map<keyof E, Array<(x: never) => never>>();
  on<K extends keyof E>(key: K, fn: (x: E[K]) => E[K]): () => void {
    const list = this.handlers.get(key) ?? []; list.push(fn as (x: never) => never); this.handlers.set(key, list);
    return () => { const i = list.indexOf(fn as (x: never) => never); if (i >= 0) list.splice(i, 1); };
  }
  run<K extends keyof E>(key: K, initial: E[K]): E[K] {
    return (this.handlers.get(key) ?? []).reduce((x, f) => f(x as never) as E[K], initial);
  }
}

const bus = new Waterfall<Events>();
const off = bus.on("normalize", x => x.trim()); bus.on("normalize", x => x.toUpperCase());
assert(bus.run("normalize", " a ") === "A", "positive ordered fold");
off(); assert(bus.run("normalize", " a ") === " A ", "negative: removed listener no longer runs");
assert(new Waterfall<Events>().run("normalize", "edge") === "edge", "boundary zero listeners");
console.log("172 ok; hands-on: reverse registration and document the changed result");
