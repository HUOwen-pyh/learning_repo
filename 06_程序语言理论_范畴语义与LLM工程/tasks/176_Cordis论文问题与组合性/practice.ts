type Context = ReadonlyMap<string, string>;
type Change = { key: string; next: string | undefined };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function apply(ctx: Context, change: Change): { next: Context; undo: Change } {
  const next = new Map(ctx); const previous = next.get(change.key);
  if (change.next === undefined) next.delete(change.key); else next.set(change.key, change.next);
  return { next, undo: { key: change.key, next: previous } };
}
function equal(a: Context, b: Context): boolean { return JSON.stringify([...a].sort()) === JSON.stringify([...b].sort()); }

const initial = new Map([["tool", "v1"]]); const step = apply(initial, { key: "tool", next: "v2" });
assert(equal(apply(step.next, step.undo).next, initial), "positive temporal recovery");
assert(!equal(step.next, initial), "negative before undo");
const noop = apply(new Map(), { key: "missing", next: undefined }); assert(equal(noop.next, new Map()), "boundary absent delete");
console.log("176 ok; hands-on: add a dependency predicate and exhibit all four composability quadrants");
