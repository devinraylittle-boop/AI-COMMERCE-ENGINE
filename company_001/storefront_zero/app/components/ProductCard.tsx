import Link from "next/link";
import type { Product } from "../lib/catalog";
import { ProductSketch } from "./ProductSketch";

export function ProductCard({ product, index }: { product: Product; index: number }) {
  return <article className="product-card"><div className="product-card-top"><span>0{index}</span><span>Candidate / verification pending</span></div><Link className="product-art-link" href={`/products/${product.slug}`} aria-label={`View ${product.name}`}><ProductSketch kind={product.kind} /></Link><div className="product-card-copy"><p className="product-verb">{product.verb}</p><h3>{product.name}</h3><p>{product.oneLine}</p><div className="product-card-footer"><span>Price pending real economics</span><Link className="round-link" href={`/products/${product.slug}`} aria-label={`Read about ${product.name}`}>→</Link></div></div></article>;
}
