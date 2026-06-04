# Design GC Skill

Codex skill for webpage design work: it recommends three distinct visual directions from a local `DESIGN.md` corpus, builds previews for each direction, asks the user to choose one, then develops the selected webpage.

## Install

One-line install:

```bash
npx skills add zhoulongyu957-sys/design-gc
```

If your shell has trouble with the Chinese repository name, use the full GitHub URL:

```bash
npx skills add https://github.com/zhoulongyu957-sys/design-gc
```

Local install during development:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/design-gc" ~/.codex/skills/design-gc
```

## Design Corpus

This skill expects a local `design-md` corpus. It works well with the MIT-licensed [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) collection.

```bash
git clone https://github.com/VoltAgent/awesome-design-md.git
export DESIGN_MD_ROOT="$(pwd)/awesome-design-md/design-md"
```

You can also pass the corpus path per command:

```bash
python3 design-gc/scripts/suggest_styles.py \
  --design-root ./awesome-design-md/design-md \
  --brief "Build a warm premium homestay booking page" \
  --top 9
```

## Use

Invoke the skill in Codex:

```text
Use $design-gc to design a landing page for a boutique homestay booking site.
```

The workflow is intentionally two-stage:

1. Recommend three materially different design directions.
2. Build previews for all three.
3. Wait for the user to choose A, B, or C.
4. Fully implement the selected direction.

## Attribution

The generated style catalog is derived from local `DESIGN.md` files. If you publish generated catalogs based on third-party corpora, preserve that corpus's license and attribution. The recommended corpus, `VoltAgent/awesome-design-md`, is MIT licensed; see `THIRD_PARTY_NOTICES.md`.
