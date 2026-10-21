# Designing Data-Intensive Applications — Interactive Reader

A complete, self-contained e-book reader with a fully Arabic (RTL) interface, built
with plain HTML, CSS and JavaScript. No frameworks, no network dependencies. Open
`index.html` directly in a browser — no server and no internet connection needed.

`book-ar.md` holds the full Arabic text of the book (about 232k words) in Markdown;
`assets/book.js` is a bundled copy of it that feeds the reader.

---

## Project layout

| Path | Purpose |
|---|---|
| `index.html` | The reader page |
| `assets/styles.css` | Complete design system: colours, typography, components |
| `assets/app.js` | Markdown renderer, table of contents, search, settings, interactions |
| `assets/book.js` | Bundled book text (generated) |
| `assets/figures/` | Figures extracted from the original PDF (175 images) |
| `assets/fonts/` | Local fonts: Noto Naskh Arabic, Cairo, Amiri |
| `assets/cover.png` | Miniature book cover, used as the page icon |
| `assets/page_map.json` | PDF page number to book page number map |
| `assets/figure_pages.json` | PDF page to full-page figure map |
| `book-ar.md` | Arabic book text in Markdown, same structure as the source |
| `chunks/ar/` | Translation chunks (222 files) |
| `chunks/` | Source chunks |
| `tools/` | Build and verification scripts |

---

## Design system

### Themes

Four reading modes, each with its own paper, surface and syntax colours:

| Mode | Paper |
|---|---|
| Light amber | `#fffdf4` |
| Medium amber | `#fbf2d6` |
| Cream white | `#fdfcf9` |
| Dark | `#1c1a16` |

### Per-chapter colour identity

Each chapter lives in its own `<section class="chapter" data-ch="N">` and carries a
distinct accent colour from a twelve-step palette. The entire interface follows the
chapter you are reading: the progress bar, the header rule, section headings, index
dots and list markers all re-tint as you move from chapter to chapter.

### Components

- **Chapter opener** — a gradient rule in the chapter colour, a filled
  "Chapter N" badge, then the chapter title and an accent underline.
- **Section headings** — a coloured bar on the leading edge.
- **Code examples** — a separate surface, a header bar carrying the detected
  language and a copy button, plus lightweight syntax colouring (keywords violet,
  strings green, numbers orange, comments grey italic).
- **Figures** — a soft frame with a click-to-zoom overlay.
- **Epigraphs** — an italic block with a coloured side rule and a large quote mark.
- **References** — a numbered list with hanging indents; English titles are set
  left-to-right, Arabic fragments are isolated right-to-left.
- **Reference markers** — small, raised, coloured numerals in the body text.

---

## Reader features

- **Table of contents** — a slide-in drawer built automatically (485 entries), with
  instant filtering and the current section highlighted.
- **Interactive contents page** — the book's own table of contents is rebuilt as a
  linked page: every chapter in its own colour, its sections beneath it, and the
  real page numbers of the printed book.
- **Search** — `Ctrl+F` or `/`; instant full-text search with highlighted matches
  and match-to-match navigation.
- **Chapter navigation** — buttons in the footer bar, or the `[` and `]` keys.
- **Resume reading** — the scroll position is saved and restored on reload.
- **Typography** — Noto Naskh (serif), Cairo (sans) or Amiri; type size 70–150 %;
  line height 1.40–2.40; text width 30rem–58rem.
- **Page numbers** — printed book page numbers appear as light chips in the body
  and can be switched off.
- **Reading time** — an estimate in the footer bar.
- **Print / save as PDF** — a clean, image-inclusive print stylesheet.

### Keyboard shortcuts

| Key | Action |
|---|---|
| `Ctrl+F` or `/` | Search |
| `Ctrl+B` | Toggle the contents drawer |
| `t` | Cycle the theme |
| `+` / `-` | Increase / decrease the type size |
| `[` / `]` | Previous / next chapter |
| `Enter` / `Shift+Enter` | Next / previous search match |
| `Esc` | Close whatever is open |
| `?` | Shortcut reference |

---

## Bidirectional text handling

Every Latin run is isolated with `<span class="lat">` and `unicode-bidi: isolate`,
but **without** a trailing space and **without** brackets or punctuation — otherwise
the delimiters swallow the boundaries and the Arabic and Latin runs overlap.
Reference entries use an LTR base direction with the Arabic fragments isolated
individually, so English titles read in the correct order.

---

## Build pipeline

```bash
python3 tools/split.py     # split the source into 222 chunks
python3 tools/verify.py    # check block-level parity between source and translation

# PDF-backed steps (require PyMuPDF)
VENV=/path/to/.venv/bin/python
$VENV tools/page_map.py         # map PDF page numbers to book page numbers
$VENV tools/extract_figures.py  # export figures and the full-page figure map
$VENV tools/fix_code.py         # restore code examples to their original English
$VENV tools/fix_examples.py     # restore two listings that were turned into tables
python3 tools/fix_prose.py      # repair paragraphs against the PDF text
$VENV tools/make_cover.py       # build the page icon from the cover

python3 tools/merge.py     # merge, restore heading levels, figures, TOC page
python3 tools/pack.py      # bundle book-ar.md into assets/book.js
```

`tools/verify.py` compares a structural signature for every chunk — paragraphs,
headings, bullets, numbered lists, tables, page markers — between the source and
the translation.

---

## Verification results

| Check | Result |
|---|---|
| Chunk structure | 222 of 222 matching |
| Text fidelity (every block) | full match |
| Untranslated paragraphs | 0 (apart from bibliography titles and log output) |
| Lost paragraphs | 0 |
| Figures | 175 rendered, none broken |
| Remaining tables | 2 (genuine data tables) |
| Code examples | 70 blocks, language auto-detected, all in English |
| Contents page | 113 linked entries, 105 with real page numbers |
| Reference markers | 1812 rendered as chips |
| Screen sizes and themes | 16 combinations, no overflow, no errors |
| JavaScript errors | none |
| Print export | 588 pages, 500 embedded images |
