import type { Metadata } from "next";
import { PageIntro } from "../components/PageIntro";

export const metadata: Metadata = { title: "Our recommendation standard" };
const gates = [
  ["01", "Name the real problem", "Storage cannot fix leaks, pests, mold, unsafe chemicals, or owning too much. We separate those conditions before discussing a product."],
  ["02", "Show who should not buy", "A useful recommendation has edges. We publish the spaces, people, and situations where the product is the wrong answer."],
  ["03", "Make fit knowable", "External dimensions are not enough. We need clearance, usable capacity, load, care, and compatibility stated before purchase."],
  ["04", "Compare the honest alternatives", "Sometimes the right answer is a cheaper bin. Sometimes it is a permanent upgrade. We explain when each earns its cost."],
  ["05", "Verify before we claim", "Materials, durability, performance, price, and shipping become facts only after documentation and real samples support them."],
];
export default function StandardPage() { return <><PageIntro eyebrow="Our standard / no stars required" title="Confidence comes from useful limits." copy="We do not want a five-star badge to do the thinking for you. Our job is to make the decision smaller, clearer, and easier to reverse when possible." /><section className="section-shell gates">{gates.map(([number, title, copy]) => <article key={number}><span>{number}</span><div><h2>{title}</h2><p>{copy}</p></div></article>)}</section><section className="truth-quote"><div className="section-shell"><p>Our recommendation philosophy</p><blockquote>“A product earns a place only when it solves the right problem, fits the real space, and is better than buying nothing.”</blockquote><p className="quote-note">Working standard for Storefront Zero. It will change only when real evidence earns the change.</p></div></section></>; }
