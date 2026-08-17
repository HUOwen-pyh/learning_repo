type Component = { name: string; needs: readonly string[]; provide?: string; setup: () => () => void };
type Mounted = { component: Component; dispose: () => void };
type Runtime = { services: Set<string>; mounted: Map<string, Mounted> };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function unmount(rt: Runtime, name: string): void {
  const mounted = rt.mounted.get(name);
  if (!mounted) return;
  mounted.dispose();
  rt.mounted.delete(name);
  if (mounted.component.provide) rt.services.delete(mounted.component.provide);
}

function reconcile(rt: Runtime, components: readonly Component[]): void {
  const desired = new Map(components.map(component => [component.name, component]));
  assert(desired.size === components.length, "duplicate component names");
  for (const name of [...rt.mounted.keys()]) {
    if (!desired.has(name)) unmount(rt, name);
  }
  let changed = true;
  while (changed) {
    changed = false;
    for (const [name, mounted] of [...rt.mounted]) {
      if (!mounted.component.needs.every(x => rt.services.has(x))) {
        unmount(rt, name);
        changed = true;
      }
    }
    for (const c of desired.values()) {
      const ready = c.needs.every(x => rt.services.has(x));
      if (ready && !rt.mounted.has(c.name)) {
        rt.mounted.set(c.name, { component: c, dispose: c.setup() });
        if (c.provide) rt.services.add(c.provide);
        changed = true;
      }
    }
  }
}

const log: string[] = []; const rt: Runtime = { services: new Set(), mounted: new Map() };
const components: Component[] = [{ name: "provider", needs: [], provide: "tool", setup: () => { log.push("p+"); return () => log.push("p-"); } }, { name: "consumer", needs: ["tool"], setup: () => { log.push("c+"); return () => log.push("c-"); } }];
reconcile(rt, components); assert(rt.mounted.has("consumer") && log.join(",") === "p+,c+", "positive reactive activation");
reconcile(rt, components.slice(1));
assert(!rt.mounted.has("provider") && !rt.mounted.has("consumer"), "deleting desired provider propagates consumer unload");
assert(log.includes("p-") && log.includes("c-"), "provider and dependent consumer must both be disposed");
const empty: Runtime = { services: new Set(), mounted: new Map() }; reconcile(empty, []); assert(empty.mounted.size === 0, "boundary");
console.log("182 ok; hands-on: add cycle detection and a policy layer deliberately outside composability");
