# Development Guide

## Architectural Mandates

1. **Dual-Architecture Support:** All features must explicitly support parallel
   execution across both `flatpak-automatic` (root) and `flatpak-automatic-user`
   (rootless) contexts.
2. **Notification Agnosticism:** Features must utilize the existing Jinja2
   notification pipeline (Desktop, Mail, Minimal) and avoid hardcoded standard
   out messages.
