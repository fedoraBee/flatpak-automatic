# Define version macro if not passed from command line
%if 0%{?_version:1}
%define version_macro %{_version}
%else
%define version_macro 1.0.3
%endif

Name:           flatpak-automatic
Version:        %{version_macro}
Release:        1%{?dist}
Summary:        Automated Flatpak updates with optional snapshots and mail notifications
License:        GPL-3.0-or-later
URL:            https://github.com/fedoraBee/flatpak-automatic
BuildArch:      noarch

# Source is created by 'make rpm'
Source0:        %{name}-%{version}.tar.gz

Requires:       flatpak
Requires:       snapper
Requires:       s-nail
Requires:       systemd

%description
Automates Flatpak updates with pre/post Snapper snapshots and email alerts.
Includes integrated logic to avoid unnecessary snapshots, calculates update
counts for email subjects, and provides universal compatibility by 
automatically detecting Btrfs/Snapper support before execution.

%prep
%autosetup -n %{name}-%{version}

%build
# Nothing to build

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir}

%files
%{_bindir}/flatpak-automatic
%{_unitdir}/flatpak-automatic.service
%{_unitdir}/flatpak-automatic.timer
%config(noreplace) %{_sysconfdir}/sysconfig/flatpak-automatic
%license LICENSE
%doc README.md CHANGELOG.md DEVELOPMENT.md CONTRIBUTING.md AGENTS.md

%changelog
%include %{_topdir}/changelog
