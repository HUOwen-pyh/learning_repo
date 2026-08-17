export {};

type AgentEvent =
  | { kind: "started"; runId: string }
  | { kind: "token"; text: string }
  | { kind: "finished"; usage: number };

function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
function unreachable(value: never): never { throw new Error("unhandled event: " + JSON.stringify(value)); }

function describe(event: AgentEvent): string {
  switch (event.kind) {
    case "started": return "start:" + event.runId;
    case "token": return "token:" + event.text;
    case "finished": return "usage:" + event.usage;
    default: return unreachable(event);
  }
}

const richer = { kind: "started" as const, runId: "r1", debug: true };
const structural: AgentEvent = richer;
assert(describe(structural) === "start:r1", "positive structural typing");
assert(describe({ kind: "token", text: "" }) === "token:", "boundary empty token");
let failed = false;
try { describe({ kind: "bad" } as unknown as AgentEvent); } catch { failed = true; }
assert(failed, "negative untrusted runtime value");
console.log("166 ok; hands-on: add cancel and let never reveal every missing consumer");
