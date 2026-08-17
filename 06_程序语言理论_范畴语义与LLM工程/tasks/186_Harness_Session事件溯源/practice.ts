export {};
type CourseSessionEvent = { seq: number; kind: "message" | "replace"; text?: string; source?: number };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function surface(log: readonly CourseSessionEvent[]): string[] {
  const text = new Map<number, string>();
  const nodes: number[] = [];
  log.forEach((e, i) => {
    assert(e.seq === i, "non-contiguous seq");
    if (e.kind === "message") { text.set(e.seq, e.text ?? ""); nodes.push(e.seq); }
    else {
      const position = e.source === undefined ? -1 : nodes.indexOf(e.source);
      assert(position >= 0, "unknown replacement source");
      text.delete(e.source!); text.set(e.seq, e.text ?? ""); nodes.splice(position, 1, e.seq);
    }
  });
  return nodes.map(seq => text.get(seq)!);
}

const log: CourseSessionEvent[] = [{ seq: 0, kind: "message", text: "long" }, { seq: 1, kind: "replace", source: 0, text: "short" }];
assert(JSON.stringify(surface(log)) === JSON.stringify(["short"]), "positive replacement");
assert(JSON.stringify(surface([
  { seq: 0, kind: "message", text: "a" }, { seq: 1, kind: "message", text: "b" },
  { seq: 2, kind: "replace", source: 0, text: "a'" },
])) === JSON.stringify(["a'", "b"]), "replacement preserves its surface position");
assert(surface([]).length === 0, "boundary empty");
let failed = false; try { surface([{ seq: 0, kind: "replace", source: 9, text: "x" }]); } catch { failed = true; } assert(failed, "negative dangling source");
console.log("186 ok; hands-on: add tool call/result pairs and reject an orphan result");
