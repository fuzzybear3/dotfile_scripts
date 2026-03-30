# Fcitx5 Fix on COSMIC (Pop!_OS)

## Problem

After setting up Fcitx5, `GTK_IM_MODULE=ibus` and `QT_IM_MODULE=ibus` remain set despite `im-config` being configured for Fcitx5. Input method does not work in GTK apps.

Confirmed via:
```sh
echo $GTK_IM_MODULE   # ibus  ← wrong
echo $QT_IM_MODULE    # ibus  ← wrong
echo $XMODIFIERS      # @im=fcitx
```

## Root Cause

`/etc/profile.d/pop-im-ibus.sh` — a Pop!_OS system script that hardcodes IBus env vars for all sessions, running after `im-config` and silently overriding it.

Tracked in: **pop-os/cosmic-session#185** (no upstream fix as of 2026-03)

## Fix

```sh
sudo rm /etc/profile.d/pop-im-ibus.sh
```

Log out and back in. On native Wayland with Fcitx5, `GTK_IM_MODULE` and `QT_IM_MODULE` should be **unset** — GTK4/Qt6 use the Wayland `text-input-v3` protocol directly.

## Optional: Set env vars for GTK3 / XWayland apps

Create `~/.config/environment.d/fcitx5.conf`:
```ini
XMODIFIERS=@im=fcitx
GTK_IM_MODULE=fcitx
QT_IM_MODULE=fcitx
```
