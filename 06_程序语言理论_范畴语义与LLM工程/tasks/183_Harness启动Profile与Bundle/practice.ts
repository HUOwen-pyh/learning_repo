export {};
type Row = Readonly<{ id: string; config: string; disabled?: boolean }>;
type Patch = Readonly<{ id: string; config?: string; disabled?: boolean }>;
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
function composeEntries(layers: readonly (readonly Patch[])[]): Row[] {
  const rows = new Map<string, Row>();
  for (const layer of layers) for (const patch of layer) {
    const old = rows.get(patch.id);
    const disabled = patch.disabled ?? old?.disabled;
    rows.set(patch.id, { id: patch.id, config: patch.config ?? old?.config ?? "", ...(disabled === undefined ? {} : { disabled }) });
  }
  return [...rows.values()];
}
const bundles = [[{ id: "llm", config: "base" }], [{ id: "ui", config: "web" }]] as const;
const profile = [{ id: "llm", config: "profile" }] as const;
const home = [{ id: "ui", disabled: true }] as const;
const overlay = [{ id: "llm", config: "cli" }] as const;
const composed = composeEntries([...bundles, profile, home, overlay]);
assert(composed.find(row => row.id === "llm")?.config === "cli", "later overlay wins by stable id");
assert(composed.find(row => row.id === "ui")?.disabled === true, "home layer can disable a bundle row");
assert(composeEntries([]).length === 0, "empty profile root stays empty");
assert(composeEntries([[{ id: "x", config: "a" }], [{ id: "x", config: "b" }]]).length === 1, "patch replaces rather than duplicates an id");
console.log("183 ok; hands-on: compare this preflight with fixed-checkout dump-config provenance");
