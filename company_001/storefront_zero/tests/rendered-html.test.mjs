import assert from "node:assert/strict";
import test from "node:test";

async function render(path = "/") {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", `${process.pid}-${Date.now()}-${path}`);
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(new Request(`http://localhost${path}`, { headers: { accept: "text/html" } }), { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } }, { waitUntil() {}, passThroughOnException() {} });
}

test("renders the private Storefront Zero homepage honestly", async () => {
  const response = await render(); assert.equal(response.status, 200); const html = await response.text();
  assert.match(html, /A calmer home, without changing the house/); assert.match(html, /Private concept/); assert.match(html, /Checkout intentionally off/); assert.match(html, /noindex/); assert.doesNotMatch(html, /codex-preview|react-loading-skeleton|Add to cart/i);
});

test("renders every decision page and candidate page", async () => {
  const paths = ["/shop", "/about", "/our-standard", "/faq", "/shipping-returns", "/products/reach-under-sink-caddy", "/products/retrieve-pantry-caddy", "/products/reset-drawer-organizer"];
  for (const path of paths) { const response = await render(path); assert.equal(response.status, 200, path); const html = await response.text(); assert.match(html, /LITTLE BUILT/, path); assert.match(html, /Private concept/, path); }
});

test("keeps checkout and unearned commercial claims out of the prototype", async () => {
  for (const path of ["/", "/shop", "/products/reach-under-sink-caddy"]) { const html = await (await render(path)).text(); assert.doesNotMatch(html, /Add to cart|Buy now|Only \d+ left|five-star|free shipping/i); }
});
