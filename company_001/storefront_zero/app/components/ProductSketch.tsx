import type { ProductKind } from "../lib/catalog";

export function ProductSketch({ kind, large = false }: { kind: ProductKind; large?: boolean }) {
  return <div className={`product-sketch sketch-${kind} ${large ? "sketch-large" : ""}`} aria-hidden="true"><div className="sketch-object"><span /><span /><span /></div><div className="sketch-shadow" /></div>;
}
