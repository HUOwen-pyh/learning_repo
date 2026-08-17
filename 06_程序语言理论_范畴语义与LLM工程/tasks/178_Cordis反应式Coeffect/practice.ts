type State = Readonly<Record<string, string | undefined>>;
type Watcher = { name: string; needs: ReadonlySet<string> };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function notified(before: State, after: State, watcher: Watcher): boolean {
  return [...watcher.needs].some(key => before[key] !== after[key]);
}
function isolate(state: State, visible: ReadonlySet<string>): State {
  return Object.fromEntries(Object.entries(state).filter(([key]) => visible.has(key)));
}

const w: Watcher = { name: "agent", needs: new Set(["llm", "tools"]) };
assert(notified({ llm: "a" }, { llm: "b" }, w), "positive relevant change");
assert(!notified({ llm: "a", log: "1" }, { llm: "a", log: "2" }, w), "negative unrelated");
assert(!notified({}, {}, { name: "free", needs: new Set() }), "boundary empty spec");
assert(JSON.stringify(isolate({ llm: "a", secret: "x" }, new Set(["llm"]))) === JSON.stringify({ llm: "a" }), "isolation");
console.log("178 ok; hands-on: return exactly which watched keys changed, not only a boolean");
