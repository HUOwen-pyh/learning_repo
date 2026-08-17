type Op =
  | { kind: "literal"; text: string }
  | { kind: "select"; choices: readonly string[]; pick: number }
  | { kind: "fork"; branches: readonly (readonly Op[])[] };

function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function run(program: readonly Op[], prefix = ""): string[] {
  let states = [prefix];
  for (const op of program) {
    if (op.kind === "literal") states = states.map(x => x + op.text);
    else if (op.kind === "select") {
      assert(op.pick >= 0 && op.pick < op.choices.length, "invalid selection");
      states = states.map(x => x + op.choices[op.pick]);
    } else {
      states = states.flatMap(x => op.branches.flatMap(branch => run(branch, x)));
    }
  }
  return states;
}

assert(JSON.stringify(run([{ kind: "literal", text: "Q" }, { kind: "fork", branches: [[{ kind: "literal", text: "A" }], [{ kind: "literal", text: "B" }]] }])) === JSON.stringify(["QA", "QB"]), "positive");
let failed = false;
try { run([{ kind: "select", choices: [], pick: 0 }]); } catch { failed = true; }
assert(failed, "negative invalid selection");
assert(JSON.stringify(run([])) === JSON.stringify([""]), "boundary empty");
console.log("164 ok; hands-on: add a generate op backed by a deterministic mock");
