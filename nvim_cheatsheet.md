# Neovim / AstroNvim Cheat Sheet

> `<Leader>` = `Space`

---

## Navigation

| Key | Action |
|-----|--------|
| `h j k l` | Left / Down / Up / Right |
| `Ctrl+h/j/k/l` | Move between splits |
| `gg` / `G` | Top / Bottom of file |
| `{` / `}` | Jump paragraph up / down |
| `Ctrl+d` / `Ctrl+u` | Scroll half page down / up |
| `%` | Jump to matching bracket |
| `]b` / `[b` | Next / Previous buffer |
| `]t` / `[t` | Next / Previous tab |

---

## File & Search (Telescope)

| Key | Action |
|-----|--------|
| `<Leader>ff` | Find files |
| `<Leader>fg` | Live grep (search text) |
| `<Leader>fb` | Find buffers |
| `<Leader>fr` | Recent files |
| `<Leader>fh` | Find help tags |
| `<Leader>fc` | Find commands |
| `<Leader>fk` | Find keymaps |

---

## Buffers

| Key | Action |
|-----|--------|
| `<Leader>bd` | Close buffer (pick from tabline) |
| `<Leader>bc` | Close all other buffers |
| `<Leader>bs` | Sort buffers |
| `]b` / `[b` | Next / Previous buffer |

---

## LSP

| Key | Action |
|-----|--------|
| `gd` | Go to definition |
| `gD` | Go to declaration |
| `gr` | Go to references |
| `gI` | Go to implementation |
| `K` | Hover documentation |
| `<Leader>lf` | Format file |
| `<Leader>la` | Code actions |
| `<Leader>lr` | Rename symbol |
| `<Leader>ld` | Diagnostics list |
| `<Leader>ll` | LSP log |
| `]d` / `[d` | Next / Previous diagnostic |

---

## Git (`<Leader>g`)

| Key | Action |
|-----|--------|
| `<Leader>gg` | Lazygit (float) |
| `<Leader>gb` | Git branches |
| `<Leader>gc` | Git commits |
| `<Leader>gs` | Git status |
| `<Leader>gd` | Git diff |
| `]g` / `[g` | Next / Previous hunk |
| `<Leader>gh` | Preview hunk |
| `<Leader>gr` | Reset hunk |
| `<Leader>gS` | Stage hunk |

---

## Terminal (`<Leader>t`)

| Key | Action |
|-----|--------|
| `<Leader>tf` | Float terminal |
| `<Leader>th` | Horizontal terminal |
| `<Leader>tv` | Vertical terminal |
| `<Leader>tl` | Lazygit terminal |
| `<Leader>tn` | Node terminal |
| `<Leader>tp` | Python terminal |

---

## UI Toggles (`<Leader>u`)

| Key | Action |
|-----|--------|
| `<Leader>uf` | Toggle autoformat |
| `<Leader>uw` | Toggle word wrap |
| `<Leader>un` | Toggle line numbers |
| `<Leader>ur` | Toggle relative numbers |
| `<Leader>us` | Toggle spell check |
| `<Leader>uc` | Toggle conceal |
| `<Leader>ud` | Toggle diagnostics |

---

## Editing

| Key | Action |
|-----|--------|
| `gcc` | Toggle comment line |
| `gc` (visual) | Toggle comment selection |
| `Ctrl+/` | Toggle comment |
| `<Leader>/` | Toggle comment |
| `>` / `<` (visual) | Indent / Unindent |
| `u` / `Ctrl+r` | Undo / Redo |
| `yy` / `dd` / `p` | Yank / Delete / Paste line |
| `ciw` / `diw` | Change / Delete inner word |

---

## Splits & Windows

| Key | Action |
|-----|--------|
| `<Leader>-` | Horizontal split |
| `<Leader>\|` | Vertical split |
| `<Leader>q` | Close window |
| `Ctrl+h/j/k/l` | Navigate splits |

---

## Plugin: Copilot

| Key | Action |
|-----|--------|
| `Ctrl+l` | Accept suggestion |
| `Alt+]` | Next suggestion |
| `Alt+[` | Previous suggestion |
| `Ctrl+]` | Dismiss suggestion |

---

## Plugin: Markdown Preview (`markdown-preview-nvim`)
> Active in `.md` files only

| Key | Action |
|-----|--------|
| `<Leader>Mp` | Open browser preview |
| `<Leader>Mt` | Toggle preview |
| `<Leader>Ms` | Stop preview |

---

## Plugin: Image Paste (`img-clip-nvim`)
> Active in `.md` files only

| Key | Action |
|-----|--------|
| `<Leader>P` | Paste image from clipboard (saves to `assets/`) |

---

## Plugin: Render Markdown (`render-markdown-nvim`)

Renders markdown inline automatically — no keybinding needed. Toggle with:

| Key | Action |
|-----|--------|
| `<Leader>um` | Toggle markdown rendering |
