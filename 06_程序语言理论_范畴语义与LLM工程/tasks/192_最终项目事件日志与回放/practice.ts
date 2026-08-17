export {};
type LoggedEvent = Readonly<{ seq: number; prev: number; data: string; hash: number }>;
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }
function digest(prev: number, data: string): number { return [...data].reduce((n, c) => (n * 31 + c.charCodeAt(0)) >>> 0, prev >>> 0); }
function append(log: readonly LoggedEvent[], data: string): LoggedEvent[] { const prev = log.at(-1)?.hash ?? 0; return [...log, { seq: log.length, prev, data, hash: digest(prev, data) }]; }
function valid(log: readonly LoggedEvent[]): boolean { return log.every((e, i) => e.seq === i && e.prev === (log[i - 1]?.hash ?? 0) && e.hash === digest(e.prev, e.data)); }
function fork(log: readonly LoggedEvent[], length: number): LoggedEvent[] { assert(length >= 0 && length <= log.length, "bad fork length"); return log.slice(0, length).map(e => ({ ...e })); }
let log: LoggedEvent[] = append([], "a"); log = append(log, "b"); assert(valid(log), "positive chain");
assert(!valid([{ ...log[0], data: "x" }, log[1]]), "negative tamper");
const child = fork(log, 1); const extended = append(child, "c"); assert(log.length === 2 && extended.length === 2 && extended[1].data === "c", "fork independence");
assert(valid([]), "boundary empty");
console.log("192 ok; hands-on: replace digest with an injected cryptographic HashPort");
