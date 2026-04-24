# Makefile for flatpak-automatic

NAME := flatpak-automatic
EPOCH := 1
VERSION := 1.3.4
REL_NUM := 1
DATE := $(shell LC_ALL=C date +"%a %b %d %Y")
AUTHOR := "fedoraBee <9395414+fedoraBee@users.noreply.github.com>"
TOPDIR := $(CURDIR)/.rpmbuild

PREFIX ?= /usr
SYSCONFDIR ?= /etc

.PHONY: all install prep rpm rpm-build rpm-sign rpm-repo lint lint-shell lint-md lint-spec lint-rpm clean deb

all:
	@echo "Nothing to build. Use 'make install' or 'make rpm'."

prep:
	@echo "Preparing build environments..."
	mkdir -p $(TOPDIR)/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	@echo "Generating package metadata..."
	$(CURDIR)/scripts/update-package-metadata.py --epoch $(EPOCH) --version $(VERSION) --rel-num $(REL_NUM) --spec-in $(CURDIR)/rpm/$(NAME).spec.in --spec-out $(TOPDIR)/SPECS/$(NAME).spec --makefile $(CURDIR)/Makefile --date "$(DATE)" --changelog-in $(CURDIR)/CHANGELOG.md
rpm: prep rpm-build

lint: lint-shell lint-md lint-spec

lint-shell:
	shellcheck $(CURDIR)/scripts/*.sh

lint-md:
	@if command -v markdownlint > /dev/null; then \
		markdownlint --config $(CURDIR)/rpm/.markdownlint.jsonc *.md .github/**/*.md; \
	else \
		echo "Warning: markdownlint not found. Skipping markdown lint."; \
	fi

lint-spec: prep
	rpmlint -v -r $(CURDIR)/rpm/flatpak-automatic.spec.rpmlintrc --ignore-unused-rpmlintrc $(TOPDIR)/SPECS/$(NAME).spec

lint-rpm:
	rpmlint -v -r $(CURDIR)/rpm/flatpak-automatic.rpm.rpmlintrc --ignore-unused-rpmlintrc $(TOPDIR)/RPMS/noarch/*.rpm

install:
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	mkdir -p $(DESTDIR)$(SYSCONFDIR)/sysconfig
	mkdir -p $(DESTDIR)$(PREFIX)/lib/systemd/system
	install -p -m 755 scripts/flatpak-automatic.sh $(DESTDIR)$(PREFIX)/bin/flatpak-automatic
	install -p -m 644 sysconfig/flatpak-automatic $(DESTDIR)$(SYSCONFDIR)/sysconfig/flatpak-automatic
	install -p -m 644 systemd/flatpak-automatic.service $(DESTDIR)$(PREFIX)/lib/systemd/system/flatpak-automatic.service
	install -p -m 644 systemd/flatpak-automatic.timer $(DESTDIR)$(PREFIX)/lib/systemd/system/flatpak-automatic.timer

rpm-build:
	@echo "Building RPM for $(NAME) $(EPOCH):$(VERSION)-$(REL_NUM)..."
	tar -czf $(TOPDIR)/SOURCES/$(NAME)-$(VERSION).tar.gz --exclude='.git' --exclude=.rpmbuild .
	rpmbuild --define "_topdir $(TOPDIR)" -ba $(TOPDIR)/SPECS/$(NAME).spec
	@echo "RPM build complete. Output located in $(TOPDIR)/RPMS/noarch/"

rpm-sign:
	@echo "Signing RPM packages..."
	@for f in $(TOPDIR)/RPMS/noarch/*.rpm; do \
        if [ -f "$$f" ]; then \
            echo "Signing $$f..."; \
            if [ -n "$(GPG_KEY_ID)" ]; then \
                rpmsign --addsign "$$f" --define "_gpg_name $(GPG_KEY_ID)" || { \
                    echo "Conflict detected, removing old signature and re-signing..."; \
                    rpmsign --delsign "$$f"; \
                    rpmsign --addsign "$$f" --define "_gpg_name $(GPG_KEY_ID)"; \
                }; \
            elif [ "$$(rpm --eval '%{?_gpg_name}')" != "%{?_gpg_name}" ]; then \
                rpmsign --addsign "$$f" || { \
                    echo "Conflict detected, removing old signature and re-signing..."; \
                    rpmsign --delsign "$$f"; \
                    rpmsign --addsign "$$f"; \
                }; \
            else \
                echo "Error: GPG_KEY_ID is not set and %_gpg_name macro is not defined."; \
                echo "Use: make rpm-sign GPG_KEY_ID=<your-key-id> or configure ~/.rpmmacros"; \
                exit 1; \
            fi; \
        fi; \
    done

CHANNEL ?= $(or $(channel),stable)

rpm-repo:
	$(CURDIR)/scripts/update-repo.sh $(TOPDIR)/RPMS/noarch $(VERSION) $(CHANNEL) "$(GPG_KEY_ID)" $(CURDIR)/repo

clean:
	rm -rf $(TOPDIR) .debbuild *.deb

test:
	@echo "Running BATS tests..."
	bats tests/
	@echo "Running Pytest..."
	python3 -m pytest tests/

deb: prep
	@echo "Building Debian package..."
	dpkg-buildpackage -us -uc -b
	mkdir -p debs
	mv ../flatpak-automatic_* debs/ || true
