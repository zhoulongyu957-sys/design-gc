---
name: design-gc
description: Recommend three distinct webpage design directions from a local design-md corpus, generate preview interfaces for each direction, ask the user to choose one, then fully develop the selected webpage. Use when Codex is asked to design, redesign, prototype, or build a website, landing page, marketing page, dashboard, SaaS page, product page, or HTML/CSS/React/Vue/Next.js webpage and the user has not already locked a single visual style.
---

# Design GC

## Core Workflow

Use a two-stage design process: first make three strong visual directions, then build the selected one completely. Do not collapse directly into final implementation unless the user explicitly chooses a style up front.

1. Understand the request, audience, product category, desired emotion, content needs, conversion goal, and any existing app stack or design system.
2. Discover candidate styles from the design corpus. Prefer running:

```bash
python3 scripts/suggest_styles.py --brief "<user request>" --top 9
```

Set `DESIGN_MD_ROOT=/path/to/design-md` or pass `--design-root /path/to/design-md` if the corpus is not auto-detected.

3. Choose exactly three materially different directions. Avoid three variations of the same "minimal SaaS" look; vary layout rhythm, color temperature, typography, density, motion, and brand feeling.
4. Read the full `DESIGN.md` for each chosen source style before designing previews. Use `references/style-catalog.md` only as an index, not as the source of truth.
5. Present the three recommendations to the user with concise rationale, tradeoffs, and what each preview will emphasize.
6. Build a preview interface for all three directions. Use the user's actual stack when obvious; otherwise create a lightweight static preview. Each preview must include enough real page structure to judge the direction: hero, navigation, content section, cards or feature blocks, CTA, responsive behavior, and at least one meaningful motion/detail.
7. Ask the user to choose one direction. If they say "you choose", pick the strongest fit and state why.
8. Fully implement the selected page only after selection. Remove or archive unused preview-only variants if they are not meant to ship.
9. Verify the result in a browser when possible, including desktop and mobile widths.

## Style Sources

Recommended corpus:

```text
https://github.com/VoltAgent/awesome-design-md
```

Each style usually lives at:

```text
<awesome-design-md>/design-md/<brand>/DESIGN.md
```

Use the script output to find candidates, then inspect the full design document for tokens and rules: colors, typography, spacing, components, layout principles, motion, imagery, and anti-patterns. The helper script auto-detects common local clone locations such as `./design-md`, `./awesome-design-md/design-md`, and `../awesome-design-md/design-md`.

If the corpus path changes, locate it with `rg --files` or ask only if it cannot be found.

## Recommendation Format

When showing recommendations, use this compact structure:

```markdown
I recommend three directions:

A. <direction name> - inspired by <source brand/doc>
Best for: <why it fits>
Visual DNA: <palette, type, spacing, layout, imagery, motion>
Tradeoff: <what it may weaken>

B. ...

C. ...
```

Then build the previews and ask the user to pick `A`, `B`, or `C`.

## Preview Rules

Make previews feel like real design explorations, not theme swaps.

- Use different information architecture when the style demands it, not only different colors.
- Use style tokens from each `DESIGN.md`, but adapt names, content, and assets to the user's product.
- Do not use protected brand logos, exact brand copy, or misleading affiliation. Treat source styles as design references.
- Preserve an existing product's established design system when the task is clearly an incremental change inside an existing app.
- Avoid generic AI-looking purple gradients unless a chosen source explicitly calls for them.
- For frontend work, make previews load on desktop and mobile before asking the user to choose.

## Full Build Rules

After selection, implement the selected direction as production-quality frontend work:

- Consolidate design tokens into CSS variables, Tailwind config, theme files, or component styles appropriate to the repo.
- Replace preview scaffolding with maintainable components.
- Keep accessibility basics intact: semantic structure, keyboard-reachable controls, contrast, alt text or decorative image handling, and visible focus states.
- Prefer real available assets. If placeholders are necessary, make them deliberate and easy to replace.
- Run the project's relevant lint, typecheck, test, or build command when available.

## Resources

- `scripts/suggest_styles.py`: Rank and summarize design-md styles for a user brief; can also regenerate the catalog.
- `references/style-catalog.md`: Generated index of available style documents. Use it for orientation, then open the relevant full `DESIGN.md` files.
