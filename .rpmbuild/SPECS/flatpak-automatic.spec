Name:           flatpak-automatic
Epoch:          1
Version:        1.1.0
Release:        1%{?dist}
Summary:        Automated Flatpak updates with optional snapshots and mail notifications

License:        GPL-3.0-or-later
URL:            https://github.com/fedoraBee/flatpak-automatic
Source0:        https://github.com/fedoraBee/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  systemd-rpm-macros

Requires:       flatpak
Requires:       snapper
Requires:       s-nail
Requires:       systemd

%description
Automates Flatpak updates with snapshots taken before and after the update
process via Snapper, along with email alerts.
Includes integrated logic to avoid unnecessary snapshots, calculates update
counts for email subjects, and provides universal compatibility by 
automatically detecting Btrfs/Snapper support before execution.

%prep
# Use -c to create the directory before extracting, since the Makefile tar command packages the directory contents directly
%setup -q -c

%build
# Nothing to build

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir}

%check
# Basic verification of installed files in BuildRoot
#test -f ...

%post
%systemd_post %{name}.service %{name}.timer

%preun
%systemd_preun %{name}.service %{name}.timer

%postun
%systemd_postun_with_restart %{name}.service %{name}.timer

%files
%{_bindir}/flatpak-automatic
%{_unitdir}/flatpak-automatic.service
%{_unitdir}/flatpak-automatic.timer
%config(noreplace) %{_sysconfdir}/sysconfig/flatpak-automatic
%license LICENSE
%doc README.md CHANGELOG.md DEVELOPMENT.md CONTRIBUTING.md AGENTS.md

# NOTE: The %%changelog directive is automatically appended by the python script during the build process.
%changelog
* Wed Apr 22 2026 fedoraBee <9395414+fedoraBee@users.noreply.github.com> 1:1.1.0-1
- **Documentation**: Updated CONTRIBUTING.md and bug_report.md to align with project dependencies (Flatpak, Snapper, systemd) and remove legacy references.
- **Versioning**: Bumped minor version to 1.1.0 to reflect stable architectural alignment.
- **Packaging**: Expanded 'pre' to 'pre-update' in the spec description to resolve rpmlint spelling warnings.
- **Packaging**: Suppressed rpmlint warnings for missing man pages, incoherent-version-in-changelog, and empty %%preun scriptlets.

* Sun Mar 29 2026 fedoraBee <9395414+fedoraBee@users.noreply.github.com> 1.0.3
- **Build Automation:** Introduced build-rpm.sh, a dynamic helper script that extracts versioning from the SPEC file and automates the full build lifecycle.
- **Universal Compatibility:** Added filesystem safety checks to automatically detect Snapper/Btrfs support. The script now gracefully degrades to "Update-Only" mode on non-Btrfs systems.
- **Open Source Governance:** Added CONTRIBUTING.md and DEVELOPMENT.md to establish standards and local setup guides.
- **Fail-Fast Logic:** Integrated set -euo pipefail and validation checks for reliability.
- **Variable Refactoring:** Standardized environment variables to **UPPERCASE** (EMAIL_TO, EMAIL_FROM, etc.).
- **Metadata Sync:** Optimized the .spec file to include all new documentation in the %%doc payload.

* Sun Mar 29 2026 fedoraBee <9395414+fedoraBee@users.noreply.github.com> 1.0.2
- **Internal Refactor:** Improved shell logic consistency and variable validation.
- **Reporting:** Optimized notification logic with late-binding variable evaluation.

* Sun Mar 29 2026 fedoraBee <9395414+fedoraBee@users.noreply.github.com> 1.0.1
- **Dynamic Subjects:** Email subjects now include the count of updated packages using regex parsing.
- **Optimization:** Added a zero-impact dry-run check to prevent unnecessary disk writes/snapshots.
- **RPM Build:** Corrected macro path resolution for LICENSE and README.md within the buildroot.

* Thu Mar 12 2026 fedoraBee <9395414+fedoraBee@users.noreply.github.com> 1.0.0
- Initial release with Snapper pre/post snapshot integration.
- Systemd timer and service for daily automation.
- Email reporting via s-nail/mailx.
