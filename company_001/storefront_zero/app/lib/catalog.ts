export type ProductKind = "under-sink" | "pantry" | "drawer";

export type Product = {
  slug: string; shortName: string; name: string; verb: string; kind: ProductKind;
  oneLine: string; problem: string; forWhom: string; notFor: string[]; why: string[];
  cheaper: string; premium: string; unknowns: string[]; sampleChecks: string[];
};

export const brand = {
  name: "Little Built",
  promise: "Small changes. Better everyday living.",
  position: "Reversible organization for real homes.",
  principles: ["diagnose before selling", "fit before features", "truth before urgency"],
} as const;

export const products: Product[] = [
  {
    slug: "reach-under-sink-caddy", shortName: "Reach", name: "Tool-Free Under-Sink Caddy", verb: "Reach", kind: "under-sink",
    oneLine: "Bring the bottles you use forward—without drilling around the plumbing.",
    problem: "Under-sink supplies disappear behind pipes, bottles, and one another.",
    forWhom: "A dry cabinet with measured clearance and a small group of frequently used supplies.",
    notFor: ["An active leak, mold, odor, or pest issue", "Unsafe chemical combinations", "A cabinet that is simply holding too much", "Clearance that has not been measured"],
    why: ["Freestanding and removable", "Narrow enough to work around plumbing", "Designed to carry one useful group", "Washable if a bottle leaks"],
    cheaper: "Choose a plain handled bin if containment and lifting already solve the problem.",
    premium: "Choose an installed pull-out only if you need greater capacity and are ready to commit to the cabinet.",
    unknowns: ["Final dimensions and load limit", "Handle and base durability", "Verified material and cleaning behavior", "Landed cost and return risk"],
    sampleChecks: ["Fits around real plumbing without contact", "Stays stable when pulled and carried", "Contains a small bottle leak", "Survives 500 pull, lift, and reset cycles"],
  },
  {
    slug: "retrieve-pantry-caddy", shortName: "Retrieve", name: "Pull-Out Pantry Caddy", verb: "Retrieve", kind: "pantry",
    oneLine: "Move one hidden pantry category from the back of the shelf to the counter.",
    problem: "Deep shelves hide smaller packages and turn one item into a full-shelf search.",
    forWhom: "A measured shelf with one recurring category that is hard to see or reach.",
    notFor: ["Active pests or uncleaned spills", "Excess inventory disguised as a storage problem", "A shallow or weak shelf", "Loose heavy items outside the declared load"],
    why: ["Pulls one category out as a unit", "Dividers prevent a new pile from forming", "High walls contain small packages", "No cabinet hardware required"],
    cheaper: "Choose a clear bin if visibility and occasional lifting are enough.",
    premium: "Choose an installed drawer only when higher capacity justifies hardware, fit work, and permanence.",
    unknowns: ["Wheel durability and loaded pull force", "Shelf-surface compatibility", "Usable internal width", "Whether the improvement earns a premium over a bin"],
    sampleChecks: ["Rolls straight at the declared load", "Does not scratch a finished shelf", "Dividers stay seated", "Survives 1,000 loaded pull-and-return cycles"],
  },
  {
    slug: "reset-drawer-organizer", shortName: "Reset", name: "Expandable Drawer Organizer", verb: "Reset", kind: "drawer",
    oneLine: "Give everyday utensils stable zones that adapt to the drawer you already have.",
    problem: "Mixed utensils hide one another, drift, and catch when the drawer closes.",
    forWhom: "A measured drawer with useful utensils that fit its depth and top clearance.",
    notFor: ["An overfilled drawer that needs a clean-out", "A shallow or obstructed drawer", "Utensils taller than the safe top clearance", "A fixed tray that already fits well"],
    why: ["Adjusts to the available width", "Moves with you instead of altering the drawer", "Creates visible zones", "Can be removed for cleaning"],
    cheaper: "Choose a fixed tray when its dimensions already fit your drawer and utensil set.",
    premium: "Choose a custom insert only if maximizing every inch is worth less flexibility and a higher commitment.",
    unknowns: ["Expansion-lock durability", "Non-slip performance", "Material odor and cleaning", "Real utensil fit across households"],
    sampleChecks: ["Holds its width through 1,000 drawer cycles", "Stays put in a finished drawer", "Leaves safe top clearance", "Has no sharp edges, odor, or trapped-water channels"],
  },
];

export function buildStorefrontView(omittedSlugs: string[] = []) {
  return { brand, products: products.filter((product) => !omittedSlugs.includes(product.slug)) };
}

export function getProduct(slug: string) { return products.find((product) => product.slug === slug); }
