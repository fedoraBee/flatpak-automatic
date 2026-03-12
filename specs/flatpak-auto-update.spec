Name:           flatpak-auto-update
Version:        1.0.0
Release:        1%{?dist}
Summary:        Automated Flatpak updates with optional snapshots and mail notifications
License:        GPL-3.0-or-later
BuildArch:      noarch
Requires:       flatpak, snapper, s-nail, systemd

%description
Automates Flatpak updates with pre/post Snapper snapshots and email alerts.
Includes integrated logic to avoid unnecessary snapshots and provides
full command-line configurability for mail and snapshots.

%install
# 1. Create the directories
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/flatpak-auto-update
mkdir -p %{buildroot}%{_docdir}/%{name}

# 2. Install the functional files
install -p -m 755 %{_sourcedir}/flatpak-auto-update.sh %{buildroot}%{_bindir}/flatpak-auto-update
install -p -m 644 %{_sourcedir}/flatpak-auto-update.service %{buildroot}%{_unitdir}/
install -p -m 644 %{_sourcedir}/flatpak-auto-update.timer %{buildroot}%{_unitdir}/
install -p -m 644 %{_sourcedir}/env.conf %{buildroot}%{_sysconfdir}/flatpak-auto-update/env.conf
install -p -m 644 %{_sourcedir}/LICENSE %{buildroot}%{_docdir}/%{name}/LICENSE

# 3. Manual copy of the README so RPM can find it for documentation
install -p -m 644 %{_sourcedir}/README.md %{buildroot}%{_docdir}/%{name}/README.md

%files
%{_bindir}/flatpak-auto-update
%{_unitdir}/flatpak-auto-update.service
%{_unitdir}/flatpak-auto-update.timer
%dir %{_sysconfdir}/flatpak-auto-update
%config(noreplace) %{_sysconfdir}/flatpak-auto-update/env.conf
%license %{_docdir}/%{name}/LICENSE
# This tells RPM where the doc ended up in the buildroot
%doc %{_docdir}/%{name}/README.md

%changelog
* Thu Mar 12 2026 Alex <alex@localhost> - 1.0.0-2
- Added dry-run check to avoid unnecessary snapshots.
- Implemented full command-line overrides for mail and snapper.
- Added configurable email body templates.
- Updated license to GPL-3.0-or-later.

* Thu Mar 12 2026 Alex <alex@localhost> - 1.0.0-1
- Fixed README path resolution in buildroot.