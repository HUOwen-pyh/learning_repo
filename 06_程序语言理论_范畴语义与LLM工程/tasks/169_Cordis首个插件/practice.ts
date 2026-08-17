type Context = { log: string[] };
type Plugin = ((ctx: Context) => void) | { apply(ctx: Context): void };
function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

function mount(ctx: Context, plugin: Plugin): void {
  if (typeof plugin === "function") plugin(ctx); else plugin.apply(ctx);
}

const ctx: Context = { log: [] };
mount(ctx, c => c.log.push("function"));
mount(ctx, { apply: c => c.log.push("object") });
assert(ctx.log.join(",") === "function,object", "positive shapes");
let failed = false; try { mount(ctx, () => { throw new Error("boom"); }); } catch { failed = true; }
assert(failed, "negative loud apply failure");
const empty: Context = { log: [] }; ([] as Plugin[]).forEach(p => mount(empty, p)); assert(empty.log.length === 0, "boundary");
console.log("169 ok; hands-on: model a Service class plugin without importing Cordis");
