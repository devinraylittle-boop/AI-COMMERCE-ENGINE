import type { Metadata } from "next";
import { PageIntro } from "../components/PageIntro";
import { ProductCard } from "../components/ProductCard";
import { buildStorefrontView } from "../lib/catalog";

export const metadata: Metadata = { title: "Candidate collection" };

export default function ShopPage() {
  const { products } = buildStorefrontView();
  return <><PageIntro eyebrow="Candidate collection / 003" title="Three useful ideas. Zero automatic recommendations." copy="A coherent starting collection for awkward kitchen and utility storage. Each candidate is shown now so we can judge the buying experience before supplier terms or sample results tempt us into certainty." /><section className="section-shell shop-grid"><div className="collection-note"><p className="section-index">The collection test</p><h2>Reach. Retrieve. Reset.</h2><p>Remove any one product—or even two—and the promise still holds: help people make small, reversible improvements without adding more regret.</p></div><div className="product-grid">{products.map((product, index) => <ProductCard key={product.slug} product={product} index={index + 1} />)}</div></section></>;
}
