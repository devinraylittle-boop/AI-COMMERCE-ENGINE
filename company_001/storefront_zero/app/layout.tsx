import type { Metadata } from "next";
import "./globals.css";
import { SiteFooter, SiteHeader } from "./components/SiteChrome";

export const metadata: Metadata = {
  title: { default: "Little Built — Storefront Zero", template: "%s — Little Built" },
  description: "A private concept store for small, reversible home-organization improvements.",
  robots: { index: false, follow: false, nocache: true },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <a className="skip-link" href="#main-content">Skip to content</a>
        <div className="prototype-bar"><span>Private concept</span><span>Candidate products</span><span>Checkout intentionally off</span></div>
        <SiteHeader />
        <main id="main-content">{children}</main>
        <SiteFooter />
      </body>
    </html>
  );
}
