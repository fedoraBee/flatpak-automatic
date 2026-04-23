#!/usr/bin/env bats

setup() {
    export ENABLE_SNAPSHOTS="no"
    export ENABLE_EMAIL="no"
    
    # Mock flatpak binary
    mkdir -p "$BATS_TEST_DIRNAME/bin"
    cat << 'EOF' > "$BATS_TEST_DIRNAME/bin/flatpak"
#!/bin/bash
echo "Nothing to do"
EOF
    chmod +x "$BATS_TEST_DIRNAME/bin/flatpak"
    export PATH="$BATS_TEST_DIRNAME/bin:$PATH"
}

teardown() {
    rm -rf "$BATS_TEST_DIRNAME/bin"
}

@test "dry-run logic exits 0 without calling Snapper" {
    run bash scripts/flatpak-automatic.sh
    [ "$status" -eq 0 ]
}
