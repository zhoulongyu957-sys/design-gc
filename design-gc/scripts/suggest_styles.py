#!/usr/bin/env python3
"""Rank local design-md style documents for a webpage brief."""

from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter
from pathlib import Path


COMMON_ROOTS = (
    Path("design-md"),
    Path("awesome-design-md/design-md"),
    Path("awesome-design-md-main/design-md"),
    Path("../awesome-design-md/design-md"),
    Path("../awesome-design-md-main/design-md"),
)

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "build",
    "by",
    "can",
    "create",
    "design",
    "for",
    "from",
    "has",
    "i",
    "in",
    "into",
    "is",
    "it",
    "make",
    "me",
    "need",
    "of",
    "on",
    "or",
    "page",
    "site",
    "that",
    "the",
    "this",
    "to",
    "use",
    "user",
    "web",
    "website",
    "with",
}

BRAND_FAMILY = {
    "airbnb": "consumer-marketplace",
    "airtable": "productivity-collab",
    "apple": "premium-product",
    "binance": "fintech",
    "bmw": "luxury-automotive",
    "bmw-m": "luxury-automotive",
    "bugatti": "luxury-automotive",
    "cal": "productivity-collab",
    "clickhouse": "developer-saas",
    "claude": "ai-enterprise",
    "clay": "creative-media",
    "cohere": "ai-enterprise",
    "composio": "developer-saas",
    "coinbase": "fintech",
    "cursor": "developer-saas",
    "dell-1996": "enterprise-corporate",
    "elevenlabs": "ai-enterprise",
    "expo": "developer-saas",
    "ferrari": "luxury-automotive",
    "figma": "creative-media",
    "framer": "creative-media",
    "hashicorp": "developer-saas",
    "hp": "enterprise-corporate",
    "ibm": "enterprise-corporate",
    "intercom": "productivity-collab",
    "kraken": "fintech",
    "lamborghini": "luxury-automotive",
    "linear.app": "developer-saas",
    "lovable": "developer-saas",
    "mastercard": "fintech",
    "meta": "enterprise-corporate",
    "minimax": "ai-enterprise",
    "mintlify": "developer-saas",
    "miro": "creative-media",
    "mistral.ai": "ai-enterprise",
    "mongodb": "developer-saas",
    "nike": "creative-media",
    "notion": "productivity-collab",
    "nvidia": "ai-enterprise",
    "ollama": "developer-saas",
    "opencode.ai": "developer-saas",
    "pinterest": "consumer-marketplace",
    "playstation": "creative-media",
    "posthog": "developer-saas",
    "raycast": "developer-saas",
    "renault": "luxury-automotive",
    "replicate": "ai-enterprise",
    "resend": "developer-saas",
    "revolut": "fintech",
    "runwayml": "creative-media",
    "sanity": "developer-saas",
    "sentry": "developer-saas",
    "shopify": "consumer-marketplace",
    "slack": "productivity-collab",
    "spacex": "premium-product",
    "spotify": "creative-media",
    "starbucks": "hospitality-retail",
    "stripe": "fintech",
    "supabase": "developer-saas",
    "superhuman": "productivity-collab",
    "tesla": "premium-product",
    "theverge": "editorial-publisher",
    "together.ai": "ai-enterprise",
    "uber": "consumer-marketplace",
    "vercel": "developer-saas",
    "vodafone": "enterprise-corporate",
    "voltagent": "ai-enterprise",
    "warp": "developer-saas",
    "webflow": "creative-media",
    "wired": "editorial-publisher",
    "wise": "fintech",
    "x.ai": "ai-enterprise",
    "zapier": "productivity-collab",
}

FAMILY_KEYWORDS = {
    "ai-enterprise": {
        "agent",
        "ai",
        "automation",
        "enterprise",
        "foundation",
        "intelligence",
        "llm",
        "machine",
        "model",
        "research",
    },
    "consumer-marketplace": {
        "booking",
        "commerce",
        "community",
        "consumer",
        "creator",
        "delivery",
        "ecommerce",
        "home",
        "listing",
        "marketplace",
        "retail",
        "shop",
        "travel",
    },
    "creative-media": {
        "art",
        "canvas",
        "creative",
        "editor",
        "gallery",
        "image",
        "media",
        "music",
        "portfolio",
        "studio",
        "video",
        "visual",
    },
    "developer-saas": {
        "api",
        "cli",
        "cloud",
        "code",
        "database",
        "developer",
        "docs",
        "engineering",
        "infrastructure",
        "platform",
        "saas",
        "terminal",
    },
    "editorial-publisher": {
        "article",
        "culture",
        "editorial",
        "magazine",
        "news",
        "publication",
        "story",
    },
    "enterprise-corporate": {
        "b2b",
        "business",
        "corporate",
        "enterprise",
        "global",
        "hardware",
        "industry",
        "solution",
    },
    "fintech": {
        "bank",
        "banking",
        "card",
        "crypto",
        "exchange",
        "finance",
        "fintech",
        "money",
        "payment",
        "wallet",
    },
    "hospitality-retail": {
        "coffee",
        "drink",
        "food",
        "hospitality",
        "local",
        "restaurant",
        "retail",
        "store",
    },
    "luxury-automotive": {
        "auto",
        "automotive",
        "car",
        "craft",
        "luxury",
        "performance",
        "premium",
        "speed",
        "vehicle",
    },
    "premium-product": {
        "device",
        "hardware",
        "minimal",
        "premium",
        "product",
        "showcase",
        "technology",
    },
    "productivity-collab": {
        "collaboration",
        "crm",
        "dashboard",
        "ops",
        "planning",
        "productivity",
        "project",
        "team",
        "workflow",
    },
}

FAMILY_PHRASES = {
    "ai-enterprise": {
        "agent",
        "ai",
        "llm",
        "人工智能",
        "企业级ai",
        "大模型",
        "可信",
        "智能体",
        "模型",
        "研究",
    },
    "consumer-marketplace": {
        "consumer",
        "marketplace",
        "booking",
        "community",
        "生活方式",
        "消费",
        "社区",
        "电商",
        "民宿",
        "生活",
        "预订",
        "预订平台",
        "旅行",
        "温暖",
        "用户增长",
    },
    "creative-media": {
        "creative",
        "studio",
        "video",
        "作品集",
        "创作",
        "创意",
        "图片",
        "媒体",
        "视觉",
        "设计工具",
        "视频",
    },
    "developer-saas": {
        "api",
        "cli",
        "developer",
        "docs",
        "saas",
        "代码",
        "开发",
        "开发工具",
        "开发者",
        "开发者平台",
        "工程",
        "技术",
        "文档",
        "终端",
    },
    "editorial-publisher": {
        "editorial",
        "magazine",
        "内容",
        "叙事",
        "杂志",
        "新闻",
        "文章",
    },
    "enterprise-corporate": {
        "b2b",
        "business",
        "enterprise",
        "企业",
        "全球",
        "商业",
        "行业",
        "解决方案",
    },
    "fintech": {
        "crypto",
        "finance",
        "fintech",
        "付款",
        "加密",
        "支付",
        "金融",
        "钱包",
        "银行",
    },
    "hospitality-retail": {
        "coffee",
        "retail",
        "咖啡",
        "本地",
        "零售",
        "餐饮",
    },
    "luxury-automotive": {
        "automotive",
        "luxury",
        "奢华",
        "性能",
        "汽车",
        "豪华",
        "速度",
    },
    "premium-product": {
        "premium",
        "showcase",
        "产品",
        "产品展示",
        "极简",
        "科技感",
        "精致",
        "高级",
        "高端",
    },
    "productivity-collab": {
        "collaboration",
        "dashboard",
        "workflow",
        "仪表盘",
        "协作",
        "团队",
        "工作流",
        "效率",
        "生产力",
        "项目管理",
    },
}

BRAND_PHRASES = {
    "airbnb": {"booking", "home", "travel", "住宿", "民宿", "生活方式", "预订", "高端民宿"},
    "apple": {"premium", "产品", "产品展示", "精致", "科技感", "高级", "高端"},
    "claude": {"ai", "assistant", "人工智能", "可信", "对话", "智能体"},
    "cohere": {"ai", "b2b", "enterprise", "人工智能", "企业级", "可信", "大模型"},
    "cursor": {"ai", "ide", "代码", "开发工具", "开发者工具", "编辑器"},
    "linear.app": {"saas", "产品", "可信", "效率", "高级", "高级感"},
    "mistral.ai": {"ai", "developer", "人工智能", "大模型", "开发者", "技术感"},
    "ollama": {"ai", "developer", "local", "大模型", "开发者", "模型"},
    "opencode.ai": {"ai", "code", "代码", "开发工具", "开发者工具", "终端"},
    "raycast": {"launcher", "productivity", "效率", "开发者", "工具"},
    "resend": {"developer", "email", "api", "开发者", "技术感"},
    "stripe": {"checkout", "developer", "finance", "payment", "支付", "开发者"},
    "together.ai": {"ai", "api", "developer", "人工智能", "大模型", "开发者"},
    "vercel": {"developer", "platform", "saas", "官网", "开发者", "技术感", "部署"},
    "voltagent": {"agent", "ai", "developer", "人工智能", "智能体", "开发者"},
    "warp": {"ai", "developer", "terminal", "开发者", "终端"},
}


def tokenise(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9][a-z0-9.-]{2,}", text.lower())
        if token not in STOPWORDS
    ]


def extract_scalar(frontmatter: str, key: str) -> str:
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        match = re.match(rf"^{re.escape(key)}:\s*(.*)$", line)
        if not match:
            continue
        value = match.group(1).strip()
        if value in {"|", ">"}:
            block_lines: list[str] = []
            for block_line in lines[index + 1 :]:
                if block_line and not block_line.startswith(" "):
                    break
                block_lines.append(block_line.strip())
            return " ".join(part for part in block_lines if part).strip().strip("\"'")
        return value.strip("\"'")
    return ""


def extract_colors(frontmatter: str) -> dict[str, str]:
    colors: dict[str, str] = {}
    in_colors = False
    for line in frontmatter.splitlines():
        if line.strip() == "colors:":
            in_colors = True
            continue
        if in_colors and line and not line.startswith(" "):
            break
        if not in_colors:
            continue
        match = re.match(r"\s{2}([a-zA-Z0-9_-]+):\s*\"?(#[0-9a-fA-F]{3,8})\"?", line)
        if match and match.group(1) in {"primary", "canvas", "ink", "body", "accent"}:
            colors[match.group(1)] = match.group(2)
    return colors


def frontmatter_from(text: str) -> str:
    if not text.startswith("---"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) >= 3 else ""


def infer_family(slug: str, description: str) -> str:
    if slug in BRAND_FAMILY:
        return BRAND_FAMILY[slug]
    tokens = set(tokenise(f"{slug} {description}"))
    scores = {
        family: len(tokens & keywords)
        for family, keywords in FAMILY_KEYWORDS.items()
    }
    family, score = max(scores.items(), key=lambda item: item[1])
    return family if score else "general-web"


def load_styles(root: Path) -> list[dict[str, object]]:
    styles: list[dict[str, object]] = []
    for path in sorted(root.glob("*/DESIGN.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = frontmatter_from(text)
        slug = path.parent.name
        description = extract_scalar(frontmatter, "description")
        name = extract_scalar(frontmatter, "name") or slug
        family = infer_family(slug, description)
        colors = extract_colors(frontmatter)
        search_text = f"{slug} {name} {description} {text[:12000]}"
        styles.append(
            {
                "slug": slug,
                "name": name,
                "family": family,
                "description": description,
                "colors": colors,
                "path": str(path),
                "tokens": Counter(tokenise(search_text)),
                "description_tokens": set(tokenise(description)),
            }
        )
    return styles


def requested_families(brief_tokens: set[str]) -> set[str]:
    return {
        family
        for family, keywords in FAMILY_KEYWORDS.items()
        if brief_tokens & keywords
    }


def requested_family_scores(brief: str, brief_tokens: set[str]) -> dict[str, int]:
    brief_lower = brief.lower()
    scores: dict[str, int] = {}
    token_families = requested_families(brief_tokens)
    for family in token_families:
        scores[family] = scores.get(family, 0) + 1
    for family, phrases in FAMILY_PHRASES.items():
        hits = sum(1 for phrase in phrases if phrase in brief_lower)
        if hits:
            scores[family] = scores.get(family, 0) + hits
    return scores


def score_style(style: dict[str, object], brief: str) -> float:
    brief_tokens = tokenise(brief)
    family_scores = requested_family_scores(brief, set(brief_tokens))
    if not brief_tokens and not family_scores:
        return 1.0

    token_counts: Counter[str] = style["tokens"]  # type: ignore[assignment]
    description_tokens: set[str] = style["description_tokens"]  # type: ignore[assignment]
    slug = str(style["slug"]).lower()
    family = str(style["family"])
    brief_lower = brief.lower()
    score = 0.0

    for token in brief_tokens:
        if token in slug:
            score += 12
        if token in description_tokens:
            score += 6
        score += min(token_counts.get(token, 0), 8) * 0.8

    if family in family_scores:
        score += 18 + family_scores[family] * 5

    brand_hits = sum(1 for phrase in BRAND_PHRASES.get(slug, set()) if phrase in brief_lower)
    if brand_hits:
        score += brand_hits * 9

    for phrase in re.findall(r"[a-z0-9][a-z0-9 .-]{4,}", brief_lower):
        if phrase.strip() and phrase in str(style["description"]).lower():
            score += 8

    return round(score, 2)


def choose_diverse(ranked: list[dict[str, object]], count: int = 3) -> list[dict[str, object]]:
    selected: list[dict[str, object]] = []
    seen_families: set[str] = set()
    if not ranked:
        return selected
    diversity_threshold = max(6.0, float(ranked[0].get("score", 0)) * 0.45)
    for item in ranked:
        if float(item.get("score", 0)) < diversity_threshold:
            continue
        family = str(item["family"])
        if family in seen_families:
            continue
        selected.append(item)
        seen_families.add(family)
        if len(selected) == count:
            return selected
    for item in ranked:
        if item not in selected:
            selected.append(item)
        if len(selected) == count:
            return selected
    return selected


def summarize(style: dict[str, object]) -> dict[str, object]:
    return {
        "slug": style["slug"],
        "name": style["name"],
        "family": style["family"],
        "score": style.get("score", 0),
        "description": style["description"],
        "colors": style["colors"],
        "path": style["path"],
    }


def recommend(root: Path, brief: str, top: int) -> dict[str, object]:
    styles = load_styles(root)
    for style in styles:
        style["score"] = score_style(style, brief)
    ranked = sorted(styles, key=lambda item: (-float(item["score"]), str(item["slug"])))
    return {
        "brief": brief,
        "design_root": str(root),
        "recommended_three": [summarize(item) for item in choose_diverse(ranked, 3)],
        "ranked": [summarize(item) for item in ranked[:top]],
    }


def catalog_markdown(root: Path) -> str:
    styles = load_styles(root)
    lines = [
        "# Design-MD Style Catalog",
        "",
        "Source root: configurable with `DESIGN_MD_ROOT` or `--design-root`.",
        "",
        "Generated from each brand's `DESIGN.md` frontmatter. Use this as an index; read the full design document before creating previews or implementation.",
        "",
    ]
    for style in styles:
        colors = style["colors"]
        color_bits = ", ".join(f"{key} {value}" for key, value in colors.items()) or "not listed"
        doc_path = Path(str(style["path"]))
        try:
            display_path = doc_path.relative_to(root)
        except ValueError:
            display_path = doc_path
        lines.extend(
            [
                f"## {style['slug']}",
                "",
                f"- Family: `{style['family']}`",
                f"- Design doc: `{display_path}`",
                f"- Colors: {color_bits}",
                f"- DNA: {style['description']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def resolve_root(raw_root: str | None) -> Path:
    root_arg = raw_root or os.environ.get("DESIGN_MD_ROOT")
    if root_arg:
        root = Path(root_arg).expanduser()
    else:
        root = next((candidate for candidate in COMMON_ROOTS if candidate.exists()), COMMON_ROOTS[0])
    if not root.exists():
        raise SystemExit(
            f"Design corpus not found: {root}\n"
            "Clone https://github.com/VoltAgent/awesome-design-md, then set DESIGN_MD_ROOT "
            "or pass --design-root /path/to/awesome-design-md/design-md."
        )
    return root


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", default="", help="User webpage request or product brief.")
    parser.add_argument("--design-root", help="Path to the design-md directory.")
    parser.add_argument("--top", type=int, default=9, help="Number of ranked styles to print.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown.")
    parser.add_argument("--catalog", action="store_true", help="Print a Markdown catalog for all styles.")
    args = parser.parse_args()

    root = resolve_root(args.design_root)
    if args.catalog:
        print(catalog_markdown(root), end="")
        return

    result = recommend(root, args.brief, args.top)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print(f"Brief: {args.brief or '(empty)'}")
    print(f"Design root: {result['design_root']}")
    print("\nRecommended three:")
    for index, item in enumerate(result["recommended_three"], start=1):
        print(f"{index}. {item['slug']} [{item['family']}] score={item['score']}")
        print(f"   {item['description']}")
        print(f"   Doc: {item['path']}")
    print("\nRanked candidates:")
    for index, item in enumerate(result["ranked"], start=1):
        print(f"{index}. {item['slug']} [{item['family']}] score={item['score']}")


if __name__ == "__main__":
    main()
