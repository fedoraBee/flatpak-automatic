Name:           flatpak-auto-update
Version:        1.0.2
Release:        1%{?dist}
Summary:        Automated Flatpak updates with optional snapshots and mail notifications
License:        GPL-3.0-or-later
BuildArch:      noarch
Requires:       flatpak, snapper, s-nail, systemd

%description
Automates Flatpak updates with pre/post Snapper snapshots and email alerts.
Includes integrated logic to avoid unnecessary snapshots, calculates update
counts for email subjects, and provides full configurability.

%install
# 1. Create the system directories
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/flatpak-auto-update

# 2. Install the functional files from SOURCES to BUILDROOT
install -p -m 755 %{_sourcedir}/flatpak-auto-update.sh %{buildroot}%{_bindir}/flatpak-auto-update
install -p -m 644 %{_sourcedir}/flatpak-auto-update.service %{buildroot}%{_unitdir}/
install -p -m 644 %{_sourcedir}/flatpak-auto-update.timer %{buildroot}%{_unitdir}/
install -p -m 644 %{_sourcedir}/env.conf %{buildroot}%{_sysconfdir}/flatpak-auto-update/env.conf

# 3. Copy documentation to the current BUILD directory so %doc/%license can find them
cp %{_sourcedir}/README.md .
cp %{_sourcedir}/LICENSE .

%files
%{_bindir}/flatpak-auto-update
%{_unitdir}/flatpak-auto-update.service
%{_unitdir}/flatpak-auto-update.timer
%dir %{_sysconfdir}/flatpak-auto-update
%config(noreplace) %{_sysconfdir}/flatpak-auto-update/env.conf

# Documentation macros look in the current BUILD directory
%license LICENSE
%doc README.md

%changelog
* Sun Mar 29 2026 Alex <alex@localhost> - 1.0.2-1
- Standardized configuration variables to UPPERCASE (EMAIL_TO, EMAIL_FROM).
- Improved internal script consistency and documentation.

* Sun Mar 29 2026 Alex <alex@localhost> - 1.0.1-1
- Fixed macro path resolution for LICENSE and README.
- Added dynamic package count to email subject line.
- Optimized shell logic with template evaluation for notifications.