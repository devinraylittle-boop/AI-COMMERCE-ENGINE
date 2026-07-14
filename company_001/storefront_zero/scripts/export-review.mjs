import { copyFile, mkdir, readdir, rm, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const siteRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const outputRoot = resolve(siteRoot, "..", "storefront", "review", "storefront-zero-html");
const workerUrl = new URL("../dist/server/index.js", import.meta.url);
workerUrl.searchParams.set("export", `${Date.now()}`);
const { default: worker } = await import(workerUrl.href);

const pages = [
  ["/", "index.html", "Homepage"],
  ["/shop", "02-collection.html", "Candidate collection"],
  ["/products/reach-under-sink-caddy", "03-reach-under-sink-caddy.html", "Reach — Under-Sink Caddy"],
  ["/products/retrieve-pantry-caddy", "04-retrieve-pantry-caddy.html", "Retrieve — Pantry Caddy"],
  ["/products/reset-drawer-organizer", "05-reset-drawer-organizer.html", "Reset — Drawer Organizer"],
  ["/our-standard", "06-our-standard.html", "Recommendation standard"],
  ["/about", "07-about.html", "About"],
  ["/faq", "08-faq.html", "FAQ"],
  ["/shipping-returns", "09-shipping-returns.html", "Shipping and returns"],
];

const routeFiles = new Map(pages.map(([route, file]) => [route, file]));

function makePortable(html) {
  let result = html
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, "")
    .replace(/<link\b[^>]*rel=["']modulepreload["'][^>]*>/gi, "")
    .replaceAll('href="/assets/', 'href="assets/')
    .replaceAll("href='/assets/", "href='assets/")
    .replaceAll('src="/assets/', 'src="assets/')
    .replaceAll("src='/assets/", "src='assets/");

  for (const [route, file] of [...routeFiles.entries()].sort((a, b) => b[0].length - a[0].length)) {
    result = result.replaceAll(`href="${route}"`, `href="${file}"`);
    result = result.replaceAll(`href='${route}'`, `href='${file}'`);
  }

  return result.replace(
    "</head>",
    "<!-- Static Executive Design Review export. Runtime scripts intentionally removed. --></head>",
  );
}

await rm(outputRoot, { recursive: true, force: true });
await mkdir(outputRoot, { recursive: true });
const sourceAssets = resolve(siteRoot, "dist", "client", "assets");
const outputAssets = resolve(outputRoot, "assets");
await mkdir(outputAssets, { recursive: true });
for (const asset of await readdir(sourceAssets)) {
  if (asset.endsWith(".css")) {
    await copyFile(resolve(sourceAssets, asset), resolve(outputAssets, asset));
  }
}

for (const [route, file] of pages) {
  const response = await worker.fetch(
    new Request(`http://storefront-zero.local${route}`, { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
  if (!response.ok) throw new Error(`${route} returned ${response.status}`);
  await writeFile(resolve(outputRoot, file), makePortable(await response.text()), "utf8");
}

const manifest = [
  "# Storefront Zero HTML Export",
  "",
  "Static, offline review copy generated from the current successful server build.",
  "Runtime scripts were removed; content, responsive CSS, links, and native FAQ disclosure controls remain.",
  "",
  ...pages.map(([, file, title]) => `- [${title}](./${file})`),
  "",
  "Start with `index.html`.",
].join("\n");

await writeFile(resolve(outputRoot, "README.md"), manifest, "utf8");
console.log(outputRoot);
