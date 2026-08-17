export {};
type Phase = "idle" | "running" | "disposed";
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
class Driver {
  phase: Phase = "idle"; wakeRequested = false; cancelRequested = false; turns = 0;
  wake(): void { if (this.phase === "disposed") return; if (this.phase === "running") this.wakeRequested = true; else { this.phase = "running"; this.turns++; } }
  cancel(): void { if (this.phase === "running") this.cancelRequested = true; }
  converge(): void { if (this.phase === "disposed") return; this.phase = "idle"; this.cancelRequested = false; if (this.wakeRequested) { this.wakeRequested = false; this.wake(); } }
  dispose(): void { this.phase = "disposed"; this.wakeRequested = false; this.cancelRequested = false; }
}
const d = new Driver(); d.wake(); assert(d.phase === "running" && d.turns === 1, "idle wake");
d.wake(); assert(d.wakeRequested, "positive latch"); d.converge(); assert(d.phase === "running" && d.turns === 2 && !d.wakeRequested, "replay latch");
d.dispose(); d.wake(); assert(d.phase === "disposed" && d.turns === 2, "negative disposed drop");
const edge = new Driver(); edge.cancel(); assert(edge.phase === "idle", "boundary idle cancel");
const cancelling = new Driver(); cancelling.wake(); cancelling.cancel();
assert(cancelling.phase === "running" && cancelling.cancelRequested, "cancel signals but does not fake quiescence");
cancelling.converge(); assert(cancelling.phase === "idle" && !cancelling.cancelRequested, "drain reaches idle boundary");
console.log("187 ok; hands-on: add an inbox and prove latched wake processes exactly one queued item");
