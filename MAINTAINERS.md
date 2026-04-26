<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD033 MD041-->
<div align="center"><img src="assets/logo.svg" alt="Flatpak Automatic CLI
Banner" width="450"></div>
<!-- prettier-ignore-end -->

# Maintainers' Guide

This document outlines the processes, versioning workflows, and checklists for
project maintainers of **Flatpak Automatic**.

## GPG Signing

To sign the built RPMs, you need a GPG key. If you have configured your
`~/.rpmmacros` (as shown below), you can simply run:

```bash
make rpm-sign
```

Alternatively, you can provide the key ID directly:

```bash
make rpm-sign GPG_KEY_ID=YOUR_KEY_ID
```

### RPM GPG Configuration

You should have the following in your `~/.rpmmacros`:

```rpmMacros
%_gpg_name YOUR_KEY_ID
%_gpg_path /home/youruser/.gnupg
%__gpg /usr/bin/gpg
```

## DNF Repository Management

The project uses `createrepo_c` to maintain a DNF repository with support for
versioned channels (e.g., `v0.1/stable`, `latest/testing`).

To update the repository metadata:

```bash
make rpm-repo CHANNEL=testing GPG_KEY_ID=YOUR_KEY_ID
```

This will:

1. Organize RPMs into `repo/rpms/v<MAJOR>.<MINOR>/<CHANNEL>/`.
2. Organize DEBs into `repo/debs/v<MAJOR>.<MINOR>/<CHANNEL>/`.
3. Run `createrepo_c --update` on the RPM directory.
4. Run `dpkg-scanpackages` and `apt-ftparchive` on the DEB directory.
5. Generate signed metadata if a GPG key is provided.
6. Export the public GPG key as `repo/gpg.key`.
7. Sync the content to `repo/rpms/latest/<CHANNEL>/` and
   `repo/debs/latest/<CHANNEL>/`.

### Hosting on GitHub

To host this as a repository on GitHub:

1. The `repo` structure is staged into `public/` and deployed to the root of the
   `gh-pages` branch alongside the `index.html` landing page by the CI workflow.
2. The `repo/` contains `rpms/` and `debs/` subdirectories for each package
   type.
3. The GPG public key is available as `gpg.key` at the root of the `gh-pages`
   branch.
4. Users can then add the repository by creating a `.repo` or `.list` file
   pointing to the raw GitHub Pages URL.

## Releasing a New Version

The deployment to the public DNF repository is automated via GitHub Actions.

1. **Tag the release:** When you are ready to publish, create a new semantic
   version tag:

   ```bash
       git tag -a v0.1.0 -m "Release version 0.1.0"
   ```

2. **Push the tag:**

   ```bash
   git push origin v0.1.0
   ```

### Workflow Behavior

- **Push to `main`**: Does **not** trigger a deployment. Use this for ongoing
  development.
- **Push a `v*` tag**: Triggers the `release.yml` workflow.
  - Builds and signs the RPMs.
  - Organizes the DNF repository structure.
  - Deploys the result to the `gh-pages` branch.
  - Creates a GitHub Release with the RPMs as assets.

> ℹ️ **Note on Channels:** Tags containing `rc`, `beta`, `alpha`, or `test`
> (e.g., `v0.1.0-rc1`) are automatically deployed to the **testing** channel.
> All other tags are deployed to **stable**.

## Versioning Workflow

This project uses `tbump` as the single source of truth for versioning.

To bump the version across the `Makefile`, scripts, sysconfig, and RPM
templates:

```bash
tbump <new_version> --only-patch
```

**Do not** manually edit version strings.

## Release Checklist

Before cutting a new release, ensure the following:

- [ ] All PRs targeted for this release are merged into `main`.
- [ ] `CHANGELOG.md` is updated with the new version and release notes.
- [ ] CI pipeline (`lint`, `smoke-test`) passes on `main`.
- [ ] `tbump <version> --only-patch` has been run and committed in a PR.
- [ ] Ensure local `main` branch is synced with `origin/main`.
- [ ] Tag the release candidate (e.g.,
      `git tag -a v1.5.0-rc.1 -m "Release Candidate 1"`).
- [ ] Push the tag to trigger the automated GitHub Actions release workflow.
