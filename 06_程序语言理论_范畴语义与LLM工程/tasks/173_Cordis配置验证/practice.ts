type Config = { intervalMs: number; label: string };
type Result = { ok: true; value: Config } | { ok: false; errors: string[] };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function validate(raw: unknown): Result {
  if (typeof raw !== "object" || raw === null) return { ok: false, errors: ["$: object required"] };
  const x = raw as { intervalMs?: unknown; label?: unknown };
  const intervalMs = x.intervalMs ?? 1000; const label = x.label ?? "timer"; const errors: string[] = [];
  if (typeof intervalMs !== "number" || !Number.isFinite(intervalMs) || intervalMs < 0) errors.push("$.intervalMs: non-negative number required");
  if (typeof label !== "string") errors.push("$.label: string required");
  return errors.length ? { ok: false, errors } : { ok: true, value: { intervalMs: intervalMs as number, label: label as string } };
}

type Running = { config: Config; dispose: () => void };
class AtomicSlot {
  current?: Running;
  reconfigure(raw: unknown, start: (config: Config) => Running): Result {
    const checked = validate(raw);
    if (!checked.ok) return checked;
    let next: Running;
    try {
      next = start(checked.value);
    } catch (error) {
      return { ok: false, errors: [`$start: ${error instanceof Error ? error.message : String(error)}`] };
    }
    const previous = this.current;
    previous?.dispose();
    this.current = next;
    return checked;
  }
}

const good = validate({ intervalMs: 0, label: "x" }); assert(good.ok && good.value.intervalMs === 0, "positive and zero boundary");
const defaults = validate({}); assert(defaults.ok && defaults.value.label === "timer", "defaults");
const bad = validate({ intervalMs: "fast" }); assert(!bad.ok && bad.errors[0].startsWith("$.intervalMs"), "negative path");
const events: string[] = []; const slot = new AtomicSlot();
const start = (config: Config): Running => {
  if (config.label === "fail") throw new Error("construction failed");
  events.push(`${config.label}+`);
  return { config, dispose: () => events.push(`${config.label}-`) };
};
assert(slot.reconfigure({ label: "old" }, start).ok, "initial configuration");
const invalidSwap = slot.reconfigure({ label: 7 }, start);
assert(!invalidSwap.ok && slot.current?.config.label === "old" && events.join(",") === "old+", "validation failure preserves old instance");
const failedSwap = slot.reconfigure({ label: "fail" }, start);
assert(!failedSwap.ok && slot.current?.config.label === "old" && events.join(",") === "old+", "start failure rolls back to old instance");
assert(slot.reconfigure({ label: "new", intervalMs: 10 }, start).ok, "valid reconfiguration");
assert(slot.current?.config.label === "new" && events.join(",") === "old+,new+,old-", "validate and construct new before disposing old");
console.log("173 ok; hands-on: reject unknown keys and add a configVersion migration");
