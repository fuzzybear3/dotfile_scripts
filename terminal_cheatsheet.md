# Terminal Cheat Sheet

> Non-standard tools installed via cargo / other means.

---

## fzf — Fuzzy Finder

| Key / Command | Action |
|---------------|--------|
| `Ctrl+t` | Fuzzy-find files, insert path at cursor |
| `Ctrl+r` | Fuzzy search shell history |
| `Alt+c` | Fuzzy cd into a subdirectory |
| `**<Tab>` | Trigger fzf completion (e.g. `vim **<Tab>`) |

> `FZF_DEFAULT_COMMAND` uses `fd` — respects `.gitignore`, shows hidden files.

---

## zoxide — Smart cd

| Command | Action |
|---------|--------|
| `z <query>` | Jump to highest-frecency match |
| `z <q1> <q2>` | Narrow with multiple terms |
| `zi` | Interactive fzf picker from history |
| `z -` | Jump to previous directory |
| `zoxide query -l` | List all tracked directories |
| `zoxide add <path>` | Manually add a path |
| `zoxide remove <path>` | Remove a path from history |

---

## fd — Find Replacement

| Command | Action |
|---------|--------|
| `fd <pattern>` | Find files by name (respects `.gitignore`) |
| `fd -t f <pattern>` | Files only |
| `fd -t d <pattern>` | Directories only |
| `fd -H <pattern>` | Include hidden files |
| `fd -e rs <pattern>` | Filter by extension |
| `fd <pattern> -x <cmd>` | Run command on each result |

---

## ripgrep (rg) — Grep Replacement

| Command | Action |
|---------|--------|
| `rg <pattern>` | Search file contents recursively |
| `rg -i <pattern>` | Case-insensitive |
| `rg -t py <pattern>` | Restrict to file type |
| `rg -l <pattern>` | List matching files only |
| `rg -n <pattern>` | Show line numbers |
| `rg --hidden <pattern>` | Include hidden files |
| `rg -A 3 <pattern>` | Show 3 lines after match |

---

## bat — Cat Replacement

| Command | Action |
|---------|--------|
| `bat <file>` | View file with syntax highlighting & line numbers |
| `bat -n <file>` | Line numbers only (no decorations) |
| `bat -A <file>` | Show non-printable characters |
| `bat --language=json <file>` | Force a syntax |
| `<cmd> \| bat` | Pipe output with highlighting |

---

## exa — ls Replacement

| Command | Action |
|---------|--------|
| `exa` | List files (colored) |
| `exa -l` | Long format |
| `exa -la` | Long format + hidden files |
| `exa -T` | Tree view |
| `exa -T -L 2` | Tree, max depth 2 |
| `exa --git` | Show git status per file |

---

## bottom (btm) — System Monitor

| Command | Key in TUI | Action |
|---------|------------|--------|
| `btm` | | Launch |
| | `?` | Help |
| | `q` | Quit |
| | `Tab` | Cycle widgets |
| | `Ctrl+r` | Reset zoom |
| | `e` | Expand widget |
| | `dd` | Kill process |

---

## difftastic (difft) — Diff Tool

| Command | Action |
|---------|--------|
| `difft <file1> <file2>` | Syntax-aware diff |
| `GIT_EXTERNAL_DIFF=difft git diff` | Use with git diff |
| `GIT_EXTERNAL_DIFF=difft git log -p` | Use with git log |

---

## watchexec — Run on File Change

| Command | Action |
|---------|--------|
| `watchexec <cmd>` | Re-run cmd on any file change |
| `watchexec -e rs <cmd>` | Watch only `.rs` files |
| `watchexec -c <cmd>` | Clear screen before each run |
| `watchexec --no-vcs-ignore <cmd>` | Ignore `.gitignore` |

---

## Aliases

| Alias | Expands To |
|-------|------------|
| `python` | `python3` |
| `freecad-dev` | Launch FreeCAD with XWayland + Mesa GPU drivers |
