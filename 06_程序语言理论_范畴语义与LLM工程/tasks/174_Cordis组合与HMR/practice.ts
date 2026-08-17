type Entry = Readonly<{ id: string; module: string; config: string; disabled?: boolean }>;
type Change = Readonly<{ id: string; action: "keep" | "add" | "remove" | "replace" }>;
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function diff(oldEntries: readonly Entry[], nextEntries: readonly Entry[]): Change[] {
  const oldMap = new Map(oldEntries.map(x => [x.id, x])); const nextMap = new Map(nextEntries.map(x => [x.id, x]));
  const ids = [...new Set([...oldMap.keys(), ...nextMap.keys()])].sort();
  return ids.map(id => {
    const a = oldMap.get(id), b = nextMap.get(id);
    const wasMounted = a !== undefined && !a.disabled;
    const shouldMount = b !== undefined && !b.disabled;
    if (!wasMounted && shouldMount) return { id, action: "add" as const };
    if (wasMounted && !shouldMount) return { id, action: "remove" as const };
    if (!wasMounted && !shouldMount) return { id, action: "keep" as const };
    assert(a !== undefined && b !== undefined, "mounted entries must exist on both sides");
    return { id, action: JSON.stringify(a) === JSON.stringify(b) ? "keep" as const : "replace" as const };
  });
}

assert(diff([{ id: "a", module: "m", config: "1" }], [{ id: "a", module: "m", config: "1" }])[0].action === "keep", "positive stable id");
assert(diff([{ id: "a", module: "m", config: "1" }], [{ id: "a", module: "m", config: "2" }])[0].action === "replace", "negative: changed config cannot be kept");
assert(diff([{ id: "x", module: "m", config: "1" }], [{ id: "x", module: "m", config: "1", disabled: true }])[0].action === "remove", "enabled to disabled must unmount");
assert(diff([{ id: "x", module: "m", config: "1", disabled: true }], [{ id: "x", module: "m", config: "1" }])[0].action === "add", "disabled to enabled must mount");
assert(diff([], [{ id: "x", module: "m", config: "", disabled: true }])[0].action === "keep", "new disabled entry must not mount");
assert(diff([], []).length === 0, "boundary");
console.log("174 ok; hands-on: reject duplicate ids before diffing");
