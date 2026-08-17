export {};

type RadixEdge = { label: string[]; child: RadixNode };
type RadixNode = { terminal: boolean; edges: Map<string, RadixEdge> };

function node(terminal = false): RadixNode {
  return { terminal, edges: new Map() };
}

function commonPrefix(a: readonly string[], b: readonly string[]): number {
  let n = 0;
  while (n < a.length && n < b.length && a[n] === b[n]) n++;
  return n;
}

class NamespacedRadixTrie {
  private readonly roots = new Map<string, RadixNode>();

  insert(namespace: string, tokens: readonly string[]): void {
    let current = this.roots.get(namespace);
    if (!current) {
      current = node();
      this.roots.set(namespace, current);
    }
    let rest = [...tokens];
    if (rest.length === 0) {
      current.terminal = true;
      return;
    }

    while (rest.length > 0) {
      const edge = current.edges.get(rest[0]);
      if (!edge) {
        current.edges.set(rest[0], { label: rest, child: node(true) });
        return;
      }

      const shared = commonPrefix(rest, edge.label);
      if (shared === edge.label.length) {
        current = edge.child;
        rest = rest.slice(shared);
        if (rest.length === 0) current.terminal = true;
        continue;
      }

      // 部分重叠：把旧压缩边在最长公共前缀处拆成一个分叉节点。
      const branch = node(rest.length === shared);
      const oldSuffix = edge.label.slice(shared);
      branch.edges.set(oldSuffix[0], { label: oldSuffix, child: edge.child });
      const newSuffix = rest.slice(shared);
      if (newSuffix.length > 0) {
        branch.edges.set(newSuffix[0], { label: newSuffix, child: node(true) });
      }
      current.edges.set(rest[0], { label: edge.label.slice(0, shared), child: branch });
      return;
    }
  }

  longestPrefix(namespace: string, tokens: readonly string[]): number {
    let current = this.roots.get(namespace);
    if (!current) return 0;
    let consumed = 0;
    while (consumed < tokens.length) {
      const edge = current.edges.get(tokens[consumed]);
      if (!edge) return consumed;
      const shared = commonPrefix(tokens.slice(consumed), edge.label);
      consumed += shared;
      if (shared < edge.label.length) return consumed;
      current = edge.child;
    }
    return consumed;
  }

  debugRootLabels(namespace: string): string[] {
    return [...(this.roots.get(namespace)?.edges.values() ?? [])].map(edge => edge.label.join(" "));
  }
}

function assert(ok: unknown, message: string): asserts ok { if (!ok) throw new Error(message); }

const cache = new NamespacedRadixTrie();
cache.insert("model-A/tokenizer-v1", ["a", "b", "c"]);
cache.insert("model-A/tokenizer-v1", ["a", "b", "x"]); // 迫使 "a b c" 在 "a b" 后拆边
assert(cache.debugRootLabels("model-A/tokenizer-v1")[0] === "a b", "radix edge must split");
assert(cache.longestPrefix("model-A/tokenizer-v1", ["a", "b", "c"]) === 3, "complete hit");
assert(cache.longestPrefix("model-A/tokenizer-v1", ["a", "b", "y"]) === 2, "partial hit");
assert(cache.longestPrefix("model-B/tokenizer-v1", ["a", "b"]) === 0, "namespace isolation");
cache.insert("model-B/tokenizer-v1", ["a", "b"]);
assert(cache.longestPrefix("model-B/tokenizer-v1", ["a", "b"]) === 2, "independent namespace");
assert(cache.longestPrefix("model-A/tokenizer-v1", []) === 0, "boundary empty");
console.log("165 ok; hands-on: add reference counts and deterministic LRU eviction to radix nodes");
