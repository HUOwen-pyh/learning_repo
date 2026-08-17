export {};
type PlanEvent = { kind: "started" | "user" | "assistant" | "tool-call" | "tool-result" | "ended"; data: string };
type Port = { name: "clock" | "llm" | "tools" | "store"; required: boolean };
type Plan = { ports: readonly Port[]; events: readonly PlanEvent["kind"][] };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
function validate(plan: Plan): string[] {
  const errors: string[] = []; const names = plan.ports.map(x => x.name);
  if (new Set(names).size !== names.length) errors.push("duplicate port");
  for (const required of ["clock", "llm", "tools", "store"] as const) {
    if (!plan.ports.some(port => port.name === required && port.required)) errors.push("missing required " + required);
  }
  for (const required of ["started", "user", "assistant", "tool-call", "tool-result", "ended"] as const) if (!plan.events.includes(required)) errors.push("missing event " + required);
  return errors;
}
const good: Plan = { ports: [{ name: "clock", required: true }, { name: "llm", required: true }, { name: "tools", required: true }, { name: "store", required: true }], events: ["started", "user", "assistant", "tool-call", "tool-result", "ended"] };
assert(validate(good).length === 0, "positive architecture");
assert(validate({ ports: [], events: [] }).length >= 4, "negative incomplete");
assert(validate({ ...good, ports: [...good.ports, { name: "llm", required: true }] }).includes("duplicate port"), "boundary duplicate");
assert(validate({ ...good, ports: good.ports.map(port => port.name === "store" ? { ...port, required: false } : port) }).includes("missing required store"), "present-but-optional is not a required port");
console.log("190 ok; hands-on: add five named acceptance properties to Plan and validate uniqueness");
