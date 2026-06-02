#!/usr/bin/env bash
# card-hook.sh <label>
#
# A tiny Claude Code hook bridge for the cosmic-claude-attention-card daemon.
# Reads the hook's JSON payload from stdin, wraps it with an event label, and
# drops it (atomically) into ~/.claude/card-events/ where the daemon's poll loop
# picks it up and shows the matching card. Wired up per-event in settings.json
# (Stop=stop, StopFailure=error, PermissionRequest=permission,
# UserPromptSubmit=turnstart, Notification[idle_prompt]=idle).
#
# Must be fast and never block Claude: it only writes a small file and exits 0.

label="${1:-unknown}"
dir="$HOME/.claude/card-events"
mkdir -p "$dir" 2>/dev/null || exit 0

payload="$(cat)"
[ -z "$payload" ] && payload='{}'

base="$dir/$(date +%s%N)-$$"
printf '{"event":"%s","hook":%s}' "$label" "$payload" >"$base.tmp" 2>/dev/null &&
    mv "$base.tmp" "$base.json" 2>/dev/null

exit 0
