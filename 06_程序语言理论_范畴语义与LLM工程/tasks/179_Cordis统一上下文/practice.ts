type Internal = Readonly<{ entries: readonly [string, string][]; generation: number }>;
type Observation = Readonly<Record<string, string>>;
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function observe(state: Internal, visible: ReadonlySet<string>): Observation {
  return Object.fromEntries(state.entries.filter(([k]) => visible.has(k)).sort(([a], [b]) => a.localeCompare(b)));
}
function equivalent(a: Internal, b: Internal, visible: ReadonlySet<string>): boolean {
  return JSON.stringify(observe(a, visible)) === JSON.stringify(observe(b, visible));
}

const a: Internal = { entries: [["tool", "v1"], ["secret", "x"]], generation: 1 };
const b: Internal = { entries: [["secret", "y"], ["tool", "v1"]], generation: 9 };
assert(equivalent(a, b, new Set(["tool"])), "positive observational equality");
assert(!equivalent(a, b, new Set(["secret"])), "negative distinguishable");
assert(equivalent(a, b, new Set()), "boundary no observations");
console.log("179 ok; hands-on: add an allowed operation that exposes generation and re-evaluate equivalence");
