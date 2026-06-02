# Workstation bootstrap (Ansible)

Ansible port of `../setup_cli.py`. Runs entirely against localhost — no SSH,
no inventory of remote hosts.

## One-time setup

```bash
cd ansible
ansible-galaxy collection install -r requirements.yml
```

## Run it

```bash
# Everything (asks once for your sudo password):
ansible-playbook site.yml --ask-become-pass

# Preview without changing anything (replaces --dry-run):
ansible-playbook site.yml --ask-become-pass --check --diff

# Just one piece (replaces editing the steps[] list):
ansible-playbook site.yml --ask-become-pass --tags docker
ansible-playbook site.yml --ask-become-pass --tags "cli,fonts"
```

## Layout

| Path | Purpose |
|------|---------|
| `site.yml` | Play + ordered role list (≙ the `steps[]` array) |
| `group_vars/all.yml` | All package lists / versions / paths |
| `roles/<name>/tasks/main.yml` | One role per concern; header comments name the original `setup_cli.py` function |
| `inventory.ini` | `localhost`, local connection |
| `ansible.cfg` | Points at the inventory + roles, YAML output |

## Notes / caveats vs. the Python script

- **become**: privilege escalation is `--ask-become-pass` instead of the manual
  `getpass` + `sudo -S` / `chsh` stdin piping. Only tasks marked `become: true`
  run as root.
- **`curl | sh` installers** (rustup, oh-my-zsh, nvm, docker, tailscale, fzf)
  stay as `shell:` tasks guarded by `creates:` — Ansible doesn't improve these,
  it just gives them an idempotency guard.
- **`--check` (dry-run) is imperfect here**: the `creates:`-guarded shell tasks
  and the `uri`/version-fetch tasks don't fully simulate in check mode, so a
  check run on a fresh box reports some tasks as skipped/changed inaccurately.
  This is the one real regression vs. your hand-built `--dry-run`.
- Post-run manual steps unchanged: log out/in for the zsh + docker-group
  changes; run `sudo tailscale up`.
