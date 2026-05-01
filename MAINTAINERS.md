<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD033 MD041-->
<div align="center"><img src="assets/banner.svg" alt="Flatpak Automatic CLI
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

## Versioning & Release Workflow

This project uses `tbump` as the single source of truth for versioning and
automated changelog generation. **Do not manually edit version strings or
`CHANGELOG.md`.**

When you are ready to cut a new release, follow these steps to generate the
"Release PR":

1. **Check out a release branch:**

   ```bash
   git checkout -b release/vX.Y.Z
   ```

2. **Run tbump in no-push mode:**

   ```bash
   tbump X.Y.Z --no-push
   ```

   _Note: `tbump` will automatically trigger the `before_commit` hook, run
   `update-package-metadata.py`, generate the changelog, inject it into the RPM
   spec, and bundle everything into a single release commit and local tag._

3. **Push the branch and open a PR:**

   ```bash
   git push -u origin release/vX.Y.Z
   gh pr create --title "chore(release): vX.Y.Z" --body "Automated release PR."
   ```

4. **Merge and Push Tag:** Once the PR is merged into `main`, manually push the
   generated tag to trigger the GitHub Actions deployment:

   ```bash
   git push origin vX.Y.Z
   ```

### CI Deployment Behavior

- **Push to `main`**: Does **not** trigger a deployment. Use this for ongoing
  development.
- **Push a `v*` tag**: Triggers the `release.yml` workflow.
  - Builds and signs the RPMs/DEBs.
  - Organizes the DNF/APT repository structure.
  - Deploys the result to the `gh-pages` branch.
  - Creates a GitHub Release with the packages as assets.

> ℹ️ **Note on Channels:** Tags containing `rc`, `beta`, `alpha`, or `test`
> (e.g., `v0.1.0-rc1`) are automatically deployed to the **testing** channel.
> All other tags are deployed to **stable**.

## Release Checklist

Before running `tbump` and cutting a new release, ensure the following:

- [ ] All feature and fix PRs targeted for this release are merged into `main`.
- [ ] All merged commits adhere to Conventional Commits standards (vital for the
      changelog).
- [ ] CI pipeline (`lint`, `smoke-test`) is currently passing on `main`.
- [ ] Ensure your local `main` branch is fully synced with `origin/main`.
