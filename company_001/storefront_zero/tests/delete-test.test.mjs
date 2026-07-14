import assert from "node:assert/strict";
import test from "node:test";
import { brand, buildStorefrontView, products } from "../app/lib/catalog.ts";

test("Delete Test: the brand survives removal of one product", () => {
  const view = buildStorefrontView([products[0].slug]);
  assert.equal(view.products.length, 2); assert.equal(view.brand.promise, brand.promise); assert.equal(view.brand.position, "Reversible organization for real homes."); assert.ok(view.products.every((product) => product.oneLine.length > 20));
});

test("Delete Test: the brand survives removal of two products", () => {
  const view = buildStorefrontView([products[0].slug, products[1].slug]);
  assert.equal(view.products.length, 1); assert.equal(view.brand.promise, "Small changes. Better everyday living."); assert.deepEqual(view.brand.principles, ["diagnose before selling", "fit before features", "truth before urgency"]);
});
