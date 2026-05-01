# Flatpak Automatic

## Architecture & Deployment

`flatpak-automatic` is designed with a dual-architecture model, supporting
simultaneous parallel execution for maximum security and flexibility:

- **System-Wide (Root):** Updates global system flatpaks. Ideal for multi-user
  or enterprise fleet deployments.
- **User-Level (Rootless):** Updates user-specific flatpaks. Recommended as the
  primary, secure default for single-user desktop environments.

## Notification Capabilities

The system leverages a Jinja2 templating engine (`config/templates/`) to support
diverse delivery mechanisms:

- **Desktop Notifications:** Native OS popups for active sessions.
- **Mail Delivery:** Rich HTML and Markdown structured email reports.
- **Logging:** Formatted Markdown file logs.
- **Minimal:** Standard text outputs for quick terminal review.

## Quickstart Guide

### 1. System-Wide (Root)

```bash
sudo systemctl enable flatpak-automatic.timer
sudo systemctl start flatpak-automatic.timer
```

### 2. User-Level (Rootless)

```bash
systemctl --user enable flatpak-automatic-user.timer
systemctl --user start flatpak-automatic-user.timer
```
