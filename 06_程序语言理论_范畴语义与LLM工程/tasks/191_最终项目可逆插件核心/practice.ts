export {};
type Release = () => void;
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
class Fiber {
  private journal: Release[] = []; private dead = false;
  acquire<A>(make: () => { value: A; release: Release }): A { assert(!this.dead, "fiber disposed"); const x = make(); this.journal.push(x.release); return x.value; }
  dispose(): void { if (this.dead) return; this.dead = true; const errors: unknown[] = []; for (const release of this.journal.reverse()) try { release(); } catch (e) { errors.push(e); } this.journal = []; if (errors.length) throw new AggregateError(errors); }
}
function loadAll<A>(fiber: Fiber, makers: readonly (() => { value: A; release: Release })[]): A[] {
  try { return makers.map(make => fiber.acquire(make)); }
  catch (error) { fiber.dispose(); throw error; }
}
const log: string[] = []; const f = new Fiber(); f.acquire(() => ({ value: 1, release: () => log.push("a-") })); f.acquire(() => ({ value: 2, release: () => log.push("b-") })); f.dispose(); f.dispose();
assert(log.join(",") === "b-,a-", "positive LIFO once");
let failed = false; try { f.acquire(() => ({ value: 0, release: () => undefined })); } catch { failed = true; } assert(failed, "negative dead acquire");
const empty = new Fiber(); empty.dispose(); assert(true, "boundary empty");
const rolledBack: string[] = []; const tx = new Fiber();
failed = false; try { loadAll(tx, [() => ({ value: 1, release: () => rolledBack.push("first-") }), () => { throw new Error("second acquire"); }]); } catch { failed = true; }
assert(failed && rolledBack.join() === "first-", "later acquire failure rolls back earlier acquisition");
console.log("191 ok; hands-on: compare transactional rollback with the real Cordis spec");
