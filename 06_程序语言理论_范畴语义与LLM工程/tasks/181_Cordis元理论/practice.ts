type Op = { name: string; key: string; delta: number };
type State = Readonly<Record<string, number>>;
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function run(state: State, ops: readonly Op[]): State {
  const next = { ...state }; for (const op of ops) next[op.key] = (next[op.key] ?? 0) + op.delta; return next;
}
function same(a: State, b: State): boolean { return JSON.stringify(Object.entries(a).sort()) === JSON.stringify(Object.entries(b).sort()); }
function permutations<T>(xs: readonly T[]): T[][] {
  if (xs.length === 0) return [[]];
  return xs.flatMap((x, i) => permutations([...xs.slice(0, i), ...xs.slice(i + 1)]).map(rest => [x, ...rest]));
}

const independent: Op[] = [{ name: "a", key: "x", delta: 1 }, { name: "b", key: "y", delta: 2 }];
const finals = permutations(independent).map(order => run({}, order));
assert(finals.every(x => same(x, finals[0])), "positive finite confluence witness");
const overwrite = (state: State, key: string, value: number): State => ({ ...state, [key]: value });
assert(!same(overwrite(overwrite({}, "x", 1), "x", 2), overwrite(overwrite({}, "x", 2), "x", 1)), "negative conflict");
assert(permutations([]).length === 1, "boundary empty schedule");
console.log("181 ok; hands-on: reject cyclic dependency graphs before exploring schedules");
