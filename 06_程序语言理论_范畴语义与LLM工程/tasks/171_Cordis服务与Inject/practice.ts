type Plugin = { name: string; inject: readonly string[]; active: boolean };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function reconcile(services: ReadonlySet<string>, plugins: readonly Plugin[]): string[] {
  const changed: string[] = [];
  for (const p of plugins) {
    const ready = p.inject.every(name => services.has(name));
    if (ready !== p.active) { p.active = ready; changed.push((ready ? "load:" : "unload:") + p.name); }
  }
  return changed;
}

const consumer: Plugin = { name: "consumer", inject: ["greeter"], active: false };
assert(reconcile(new Set(), [consumer]).length === 0 && !consumer.active, "pending boundary");
assert(reconcile(new Set(["greeter"]), [consumer])[0] === "load:consumer", "positive");
assert(reconcile(new Set(), [consumer])[0] === "unload:consumer", "negative lost dependency");
const free: Plugin = { name: "free", inject: [], active: false };
assert(reconcile(new Set(), [free])[0] === "load:free", "empty dependency");
console.log("171 ok; hands-on: restore greeter and count consumer restart generations");
