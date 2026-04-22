%{!?_version: %define _version X.Y.Z}

Name:           flatpak-automatic
Version:        %{_version}
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

%check
# Basic verification of installed files in BuildRoot
#test -f ...

%global systemd_runtime_check [ -d /run/systemd/system ] && command -v systemctl >/dev/null 2>&1


%post
# Reload for the generator to pick up new user-level Quadlets
if %{systemd_runtime_check}; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi

%postun
if %{systemd_runtime_check}; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun

%files
%{_bindir}/flatpak-automatic
%{_unitdir}/flatpak-automatic.service
%{_unitdir}/flatpak-automatic.timer
%config(noreplace) %{_sysconfdir}/sysconfig/flatpak-automatic
%license LICENSE
%doc README.md CHANGELOG.md DEVELOPMENT.md CONTRIBUTING.md AGENTS.md

%changelog
%include %{_topdir}/changelog
