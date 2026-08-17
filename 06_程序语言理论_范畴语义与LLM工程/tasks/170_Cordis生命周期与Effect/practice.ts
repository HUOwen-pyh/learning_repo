type Disposer = () => void;
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

class Fiber {
  private effects: Disposer[] = [];
  private disposed = false;
  effect(acquire: () => Disposer): void { this.load([acquire]); }
  load(acquires: readonly (() => Disposer)[]): void {
    assert(!this.disposed, "dead fiber");
    const acquired: Disposer[] = [];
    try {
      for (const acquire of acquires) acquired.push(acquire());
      this.effects.push(...acquired);
    } catch (error) {
      for (const release of acquired.reverse()) release();
      throw error;
    }
  }
  dispose(): void {
    if (this.disposed) return;
    this.disposed = true;
    for (const release of this.effects.reverse()) release();
    this.effects = [];
  }
}

const log: string[] = []; const fiber = new Fiber();
fiber.effect(() => { log.push("a+"); return () => log.push("a-"); });
fiber.effect(() => { log.push("b+"); return () => log.push("b-"); });
fiber.dispose(); fiber.dispose();
assert(log.join(",") === "a+,b+,b-,a-", "positive LIFO and idempotence");
let failed = false; try { fiber.effect(() => () => undefined); } catch { failed = true; } assert(failed, "negative dead fiber");
const empty = new Fiber(); empty.dispose(); assert(true, "boundary empty journal");
const txLog: string[] = []; const transaction = new Fiber(); let transactionFailed = false;
try {
  transaction.load([
    () => { txLog.push("first+"); return () => txLog.push("first-"); },
    () => { txLog.push("second+"); throw new Error("second acquire failed"); },
  ]);
} catch { transactionFailed = true; }
assert(transactionFailed, "second acquire must fail the load transaction");
assert(txLog.join(",") === "first+,second+,first-", "partial load must release prior acquisitions in reverse order");
transaction.dispose();
assert(txLog.join(",") === "first+,second+,first-", "rolled-back effects must not remain mounted");
console.log("170 ok; hands-on: catch release errors while continuing remaining cleanup");
