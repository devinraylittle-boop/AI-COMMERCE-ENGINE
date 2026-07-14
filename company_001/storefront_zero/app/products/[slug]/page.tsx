import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ProductSketch } from "../../components/ProductSketch";
import { getProduct, products } from "../../lib/catalog";

export function generateStaticParams() { return products.map(({ slug }) => ({ slug })); }
export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> { const product = getProduct((await params).slug); return { title: product?.name ?? "Candidate product" }; }

export default async function ProductPage({ params }: { params: Promise<{ slug: string }> }) {
  const product = getProduct((await params).slug); if (!product) notFound();
  return <>
    <section className="product-hero section-shell"><div className="product-visual-wrap"><div className="concept-stamp">Concept<br />not for sale</div><ProductSketch kind={product.kind} large /></div><div className="product-summary"><p className="eyebrow">{product.shortName} / founding candidate</p><h1>{product.name}</h1><p className="product-lede">{product.oneLine}</p><div className="pending-price"><span>Price</span><strong>Pending verified economics</strong></div><button className="button button-disabled" disabled>Not available — verification pending</button><p className="fine-print">No waitlist. No invented urgency. No order accepted before fit, quality, claims, and economics are verified.</p></div></section>
    <section className="section-shell diagnosis-grid rule-top"><div><p className="section-index">The job</p><h2>{product.problem}</h2><p>{product.forWhom}</p></div><aside className="no-buy-box"><p className="eyebrow">Do not buy this for</p><ul>{product.notFor.map((item) => <li key={item}>{item}</li>)}</ul></aside></section>
    <section className="detail-band"><div className="section-shell detail-grid"><div><p className="eyebrow light">Why this form</p><h2>A tool should earn the space it occupies.</h2></div><ul className="feature-list">{product.why.map((item, index) => <li key={item}><span>0{index + 1}</span>{item}</li>)}</ul></div></section>
    <section className="section-shell compare-grid"><article><p className="eyebrow">Spend less when</p><h3>The simple answer works.</h3><p>{product.cheaper}</p></article><article><p className="eyebrow">Spend more when</p><h3>The commitment earns it.</h3><p>{product.premium}</p></article></section>
    <section className="section-shell evidence-grid rule-top"><div><p className="eyebrow">What we still do not know</p><h2>Unknown is a status, not a flaw to hide.</h2><ul className="plain-list">{product.unknowns.map((item) => <li key={item}>{item}</li>)}</ul></div><div className="test-card"><p className="eyebrow">Before recommendation</p><h3>The sample must prove:</h3><ol>{product.sampleChecks.map((item, index) => <li key={item}><span>{index + 1}</span>{item}</li>)}</ol></div></section>
    <section className="section-shell next-product"><p>This candidate has not earned a recommendation.</p><Link className="text-link" href="/shop">Return to the collection <span aria-hidden="true">→</span></Link></section>
  </>;
}
