type State = number;
type Effect = { forward: (x: State) => State; inverse: (x: State) => State; name: string };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function run(initial: State, effects: readonly Effect[]): { value: State; recover(): State } {
  let value = initial; const journal: Effect[] = [];
  for (const effect of effects) { value = effect.forward(value); journal.push(effect); }
  return { value, recover: () => [...journal].reverse().reduce((x, e) => e.inverse(x), value) };
}

const add3: Effect = { name: "add3", forward: x => x + 3, inverse: x => x - 3 };
const times2: Effect = { name: "times2", forward: x => x * 2, inverse: x => x / 2 };
const result = run(5, [add3, times2]); assert(result.value === 16 && result.recover() === 5, "positive twisted order");
const wrong = [add3, times2].reduce((x, e) => e.inverse(x), result.value); assert(wrong !== 5, "negative same-order undo");
assert(run(7, []).recover() === 7, "boundary identity");
console.log("177 ok; hands-on: add witnessed checks inverse(forward(x))=x over a finite domain");
