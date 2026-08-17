type Example = Readonly<{ input: string; target: string }>;
type Candidate = Readonly<{ name: string; predict: (x: string) => string }>;

function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function choose(candidates: readonly Candidate[], data: readonly Example[]): Candidate {
  assert(candidates.length > 0, "no candidates");
  const scored = candidates.map((c, order) => ({ c, order, score: data.reduce((n, e) => n + Number(c.predict(e.input) === e.target), 0) }));
  scored.sort((a, b) => b.score - a.score || a.order - b.order);
  return scored[0].c;
}

const lower: Candidate = { name: "lower", predict: x => x.toLowerCase() };
const upper: Candidate = { name: "upper", predict: x => x.toUpperCase() };
assert(choose([lower, upper], [{ input: "a", target: "A" }]).name === "upper", "positive");
assert(choose([lower, upper], []).name === "lower", "boundary tie is stable");
let failed = false;
try { choose([], []); } catch { failed = true; }
assert(failed, "negative empty search space");
console.log("163 ok; hands-on: evaluate the winner on a separate held-out array");
