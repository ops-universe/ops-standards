# Website design system

Reference: https://github.com/AnkitParekh007/repoOps. React + TypeScript + Vite; route registry, static prerendering, configurable Pages base and canonical URL.

| Token | Light | Dark |
|---|---|---|
| Background | #F6F4E9 | #181D17 |
| Surface | #FFFDF5 | #222A21 |
| Text | #22291E | #F5F2DF |
| Muted | #50594B | #C2C9B6 |
| Accent | #365C2C | #D5ED91 |
| Border | #D7DBCC | #465044 |

The table above is the existing repoOps reference, not a universal palette. Every new Ops project MUST have a distinct approved light/dark palette (background, surface, text, muted, accent, border, button foreground). Use ops-ui semantic tokens and record a palette ID in .ops/project.json. No duplicate project accents; normal text/link/button contrast >= 4.5:1, plus browser accessibility checks. Preserve existing project branding until a migration is explicitly approved. The central organization uses its own indigo identity. See [palette registry](palettes.md).

Sticky responsive header, project-specific hero, bounded motion, search with Cmd/Ctrl+K, theme preference, accessible focus and reduced motion, modern footer with community and funding links. Clean URLs, sitemap, robots, social metadata and 404. Test direct navigation, keyboard, mobile and contrast. Do not use fabricated metrics.
