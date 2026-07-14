import type { Metadata } from "next";
import { PageIntro } from "../components/PageIntro";

export const metadata: Metadata = { title: "FAQ" };
const questions = [
  ["Can I buy these products?", "Not yet. Storefront Zero is a private concept used to test whether the promise, collection, and decision experience make sense before supplier outreach or sales."],
  ["Why are there no prices?", "A price without a verified product, landed cost, shipping weight, return allowance, and quality result would be theater. Prices appear only after real economics exist."],
  ["Are the dimensions final?", "No. Each product page identifies fit as an unknown until a selected sample is measured. We will not imply universal fit."],
  ["Why show reasons not to buy?", "Because the wrong purchase creates more clutter and less trust. A useful store should help a customer reject a poor fit before checkout."],
  ["Are these Little Built products?", "They are Little Built product hypotheses. No supplier, manufacturer, inventory, or final SKU has been selected."],
  ["What happens next?", "We evaluate the complete buying experience, run the Delete Test, then use what we learn to define one focused supplier conversation—only after explicit approval."],
];
export default function FaqPage() { return <><PageIntro eyebrow="Questions before checkout exists" title="The honest answer is often “not yet.”" copy="This prototype is designed to expose uncertainty, not cover it with polish." /><section className="section-shell faq-list">{questions.map(([q, a], index) => <details key={q} open={index === 0}><summary><span>0{index + 1}</span>{q}</summary><p>{a}</p></details>)}</section></>; }
