type Phase = "pending" | "active" | "withdrawing" | "disposed" | "failed";
type Fiber = { name: string; needs: readonly string[]; phase: Phase };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function step(fiber: Fiber, services: ReadonlySet<string>, retire = false): string {
  if (fiber.phase === "pending" && fiber.needs.every(x => services.has(x))) { fiber.phase = "active"; return "activate"; }
  if (fiber.phase === "active" && (retire || !fiber.needs.every(x => services.has(x)))) { fiber.phase = "withdrawing"; return "withdraw"; }
  if (fiber.phase === "withdrawing") { fiber.phase = "disposed"; return "dispose"; }
  return "stutter";
}

const f: Fiber = { name: "agent", needs: ["llm"], phase: "pending" };
assert(step(f, new Set()) === "stutter" && f.phase === "pending", "boundary unmet");
assert(step(f, new Set(["llm"])) === "activate" && f.phase === "active", "positive");
assert(step(f, new Set()) === "withdraw" && f.phase === "withdrawing", "dependency loss");
assert(step(f, new Set()) === "dispose" && f.phase === "disposed", "cleanup");
assert(step({ name: "bad", needs: [], phase: "failed" }, new Set()) === "stutter", "negative failed is not activated");
console.log("180 ok; hands-on: add a generation counter for reinstallation after dispose");
