# Makefile for flatpak-automatic

NAME := flatpak-automatic
VERSION := 1.1.0-rc1
RPM_VERSION := $(subst -,~,$(VERSION))
BUILD_DIR := $(CURDIR)/rpmbuild
RPM_DIR := $(BUILD_DIR)/RPMS/noarch
PREFIX ?= /usr
SYSCONFDIR ?= /etc

.PHONY: all install prep rpm rpm-build rpm-sign rpm-repo lint lint-shell lint-md lint-spec lint-rpm clean

all:
	@echo "Nothing to build. Use 'make install' or 'make rpm'."

prep:
	@echo "Preparing RPM build environment..."
	rm -rf $(RPM_DIR)/*.rpm
	mkdir -p $(BUILD_DIR)/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	@echo "Generating RPM changelog..."
	$(CURDIR)/scripts/update-rpm-metadata.py --version $(RPM_VERSION) --spec $(CURDIR)/rpm/$(NAME).spec --changelog-in $(CURDIR)/CHANGELOG.md --changelog-out $(BUILD_DIR)/changelog
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
	@echo "%_topdir $(BUILD_DIR)" > $(BUILD_DIR)/.rpmmacros
	@echo "%_version $(RPM_VERSION)" >> $(BUILD_DIR)/.rpmmacros
	HOME=$(BUILD_DIR) rpmlint -v -r $(CURDIR)/rpm/flatpak-automatic.spec.rpmlintrc --ignore-unused-rpmlintrc $(CURDIR)/rpm/$(NAME).spec

lint-rpm:
	rpmlint -v -r $(CURDIR)/rpm/flatpak-automatic.rpm.rpmlintrc --ignore-unused-rpmlintrc $(RPM_DIR)/*.rpm

install:
	mkdir -p $(DESTDIR)$(PREFIX)/bin
	mkdir -p $(DESTDIR)$(SYSCONFDIR)/sysconfig
	mkdir -p $(DESTDIR)$(PREFIX)/lib/systemd/system
	install -p -m 755 scripts/flatpak-automatic.sh $(DESTDIR)$(PREFIX)/bin/flatpak-automatic
	install -p -m 644 sysconfig/flatpak-automatic $(DESTDIR)$(SYSCONFDIR)/sysconfig/flatpak-automatic
	install -p -m 644 systemd/flatpak-automatic.service $(DESTDIR)$(PREFIX)/lib/systemd/system/flatpak-automatic.service
	install -p -m 644 systemd/flatpak-automatic.timer $(DESTDIR)$(PREFIX)/lib/systemd/system/flatpak-automatic.timer

rpm-build:
	@echo "Building RPM packages..."
	tar -czf $(BUILD_DIR)/SOURCES/$(NAME)-$(RPM_VERSION).tar.gz --exclude=.git --exclude=rpmbuild --transform 's|^|$(NAME)-$(RPM_VERSION)/|' .
	rpmbuild -ba $(CURDIR)/rpm/$(NAME).spec --define "_version $(RPM_VERSION)" --define "_topdir $(BUILD_DIR)"
	@echo "RPMs built in $(RPM_DIR)"

rpm-sign:
	@echo "Signing RPM packages..."
	@for f in $(RPM_DIR)/*.rpm; do \
		if [ -f "$$f" ]; then \
			echo "Signing $$f..."; \
			if [ -n "$(GPG_KEY_ID)" ]; then \
				rpmsign --addsign "$$f" --define "_gpg_name $(GPG_KEY_ID)" || { \
					echo "Conflict detected, removing old signature and re-signing..."; \
					rpmsign --delsign "$$f"; \
					rpmsign --addsign "$$f" --define "_gpg_name $(GPG_KEY_ID)"; \
				}; \
			elif [ -n "$$(rpm --eval '%{?_gpg_name}')" ]; then \
				rpmsign --addsign "$$f" || { \
					echo "Conflict detected, removing old signature and re-signing..."; \
					rpmsign --delsign "$$f"; \
					rpmsign --addsign "$$f"; \
				}; \
			else \
				echo "Error: GPG_KEY_ID is not set and %_gpg_name macro is not defined."; \
				echo "Use: make sign GPG_KEY_ID=<your-key-id> or configure ~/.rpmmacros"; \
				exit 1; \
			fi; \
		fi; \
	done

CHANNEL ?= $(or $(channel),stable)

rpm-repo:
	$(CURDIR)/scripts/update-repo.sh $(RPM_DIR) $(VERSION) $(CHANNEL) "$(GPG_KEY_ID)"

clean:
	rm -rf $(BUILD_DIR)
