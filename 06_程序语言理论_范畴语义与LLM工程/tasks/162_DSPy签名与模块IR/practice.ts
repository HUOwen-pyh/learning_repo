type Row = Record<string, string>;
type Module = { name: string; needs: readonly string[]; gives: string; run: (x: Row) => string };

function assert(ok: unknown, message: string): asserts ok {
  if (!ok) throw new Error(message);
}

function execute(modules: readonly Module[], input: Row): Row {
  const env: Row = { ...input };
  for (const module of modules) {
    for (const key of module.needs) assert(key in env, module.name + " missing " + key);
    env[module.gives] = module.run(env);
  }
  return env;
}

const pipeline: Module[] = [
  { name: "normalize", needs: ["question"], gives: "normalized", run: x => x.question.trim().toLowerCase() },
  { name: "answer", needs: ["normalized"], gives: "answer", run: x => x.normalized === "2+2" ? "4" : "unknown" },
];

assert(execute(pipeline, { question: " 2+2 " }).answer === "4", "positive");
let failed = false;
try { execute(pipeline, {}); } catch { failed = true; }
assert(failed, "negative missing field");
assert(execute([], { x: "edge" }).x === "edge", "boundary empty pipeline");
console.log("162 ok; hands-on: add a typed rationale module before answer");
