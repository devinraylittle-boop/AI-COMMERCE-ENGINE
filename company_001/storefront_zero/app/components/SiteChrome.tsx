import Link from "next/link";

export function SiteHeader() {
  return <header className="site-header"><div className="section-shell header-inner"><Link className="wordmark" href="/" aria-label="Little Built home"><span className="wordmark-mark">LB</span><span>LITTLE BUILT</span></Link><nav aria-label="Primary navigation"><Link href="/shop">Shop concept</Link><Link href="/our-standard">Our standard</Link><Link href="/about">About</Link><Link href="/faq">FAQ</Link></nav></div></header>;
}

export function SiteFooter() {
  return <footer className="site-footer"><div className="section-shell footer-grid"><div><div className="wordmark footer-wordmark"><span className="wordmark-mark">LB</span><span>LITTLE BUILT</span></div><p>Small changes. Better everyday living.</p></div><div><p className="footer-label">Explore</p><Link href="/shop">Candidate collection</Link><Link href="/our-standard">Recommendation philosophy</Link><Link href="/about">About us</Link></div><div><p className="footer-label">Before launch</p><Link href="/faq">FAQ</Link><Link href="/shipping-returns">Shipping &amp; returns</Link></div><div className="footer-note"><p>Storefront Zero is a private evaluation prototype. It accepts no orders, collects no customer data, and makes no claim that candidate products are ready for sale.</p></div></div></footer>;
}
