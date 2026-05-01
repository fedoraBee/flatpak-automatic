#!/usr/bin/env bash
set -euo pipefail

# -----------------------------
# GitOps PR CLI Tool
# Release-aware + RPM + CI integration
# -----------------------------

if ! command -v gh &>/dev/null; then
    echo "❌ Error: GitHub CLI (gh) is not installed."
    exit 1
fi

# -----------------------------
# Usage
# -----------------------------
usage() {
    cat <<EOF
GitOps PR CLI Tool v4 (Conventional Commits Aware)

Usage:
  $(basename "$0") [options]

Required:
  -t, --target BRANCH  Target/Head branch (feat/vX.Y.Z-description)

Optional:
  -b, --base BASE      Base branch (default: main)
  -T, --title TITLE    PR title (default: auto-generated from commits)
  -m, --message BODY   PR body (default: auto-generated)
  -R, --reviewers USER Reviewers (comma-separated)
  -r, --remote REMOTE  Remote name (default: origin)
  --dry-run            Simulate actions without making changes
  -h, --help           Show this help

Examples:
  $(basename "$0") -t feat/v0.2.0-login-fix
  $(basename "$0") -b main -t feat/v0.2.0-login-fix -T "Fix login issue" -m "Detailed description"
  $(basename "$0") -t feat/v0.2.0-login-fix -R reviewer1,reviewer2 --dry-run
EOF
}

REMOTE="origin"
BASE_BRANCH="main"
TARGET_BRANCH=""
PR_TITLE=""
PR_BODY=""
REVIEWERS=""
DRY_RUN=false

# -----------------------------
# Parse args
# -----------------------------
while [[ $# -gt 0 ]]; do
    case "$1" in
        -b | --base)
            BASE_BRANCH="$2"
            shift 2
            ;;
        -t | --target)
            TARGET_BRANCH="$2"
            shift 2
            ;;
        -T | --title)
            PR_TITLE="$2"
            shift 2
            ;;
        -m | --message)
            PR_BODY="$2"
            shift 2
            ;;
        -R | --reviewers)
            REVIEWERS="$2"
            shift 2
            ;;
        -r | --remote)
            REMOTE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -h | --help)
            usage
            exit 0
            ;;
        -*)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
        *) shift ;;
    esac
done

# -----------------------------
# Validation
# -----------------------------
if [[ -z "$TARGET_BRANCH" ]]; then
    echo "❌ Error: Missing required argument: --target/-t."
    usage
    exit 1
fi

# Branch naming enforcement
if [[ ! "$TARGET_BRANCH" =~ ^(feat|fix|chore|refactor|docs|ci|style|test|revert|perf|build|format|deps|sec)/v[0-9]+\.[0-9]+\.[0-9]+- ]]; then
    echo "❌ Invalid branch name: $TARGET_BRANCH"
    echo "Expected: <type>/v<version>-<description>"
    exit 1
fi

# Extract version (Used for labeling/context, but not strictly validated against files anymore)
if [[ "$TARGET_BRANCH" =~ v([0-9]+\.[0-9]+\.[0-9]+) ]]; then
    VERSION="${BASH_REMATCH[1]}"
else
    echo "❌ Could not extract version from branch"
    exit 1
fi

# -----------------------------
# Dry-run checks
# -----------------------------
if [[ "$DRY_RUN" == true ]]; then
    echo "🚨 [DRY-RUN] Simulating actions..."
    echo "Remote: $REMOTE"
    echo "Base branch: $BASE_BRANCH"
    echo "Target branch: $TARGET_BRANCH"
    echo "PR title: ${PR_TITLE:-auto-generated}"
    echo "PR body: ${PR_BODY:-auto-generated}"
    echo "Reviewers: ${REVIEWERS:-none}"
    echo "Targeting Milestone: v$VERSION"
    echo "🚨 [DRY-RUN] ... no changes were made."
    exit 0
fi

echo "📦 Targeting version milestone: v$VERSION"

# -----------------------------
# Git safety checks
# -----------------------------
echo "🔍 Checking base branch ..."
git ls-remote --exit-code --heads "$REMOTE" "$BASE_BRANCH" >/dev/null || {
    echo "❌ Git branch '$BASE_BRANCH' does not exist in the remote repository ($REMOTE)."
    exit 1
}

echo "🔍 Fetching base branch from $REMOTE ..."
git fetch "$REMOTE" "$BASE_BRANCH" --quiet || {
    echo "❌ Failed to fetch base branch. Check your network and remote configuration."
    exit 1
}

echo "🔍 Checking for uncommitted changes..."
if [[ -n "$(git status --porcelain)" ]]; then
    echo "❌ Working tree is not clean. Commit or stash changes first."
    exit 1
fi

# -----------------------------
# Create / switch branch
# -----------------------------
if git show-ref --verify --quiet "refs/heads/$TARGET_BRANCH"; then
    echo "🔀 Switching to existing branch: $TARGET_BRANCH"
    git switch "$TARGET_BRANCH" --quiet
else
    echo "🌱 Creating branch: $TARGET_BRANCH"
    git switch -c "$TARGET_BRANCH" --quiet
fi

# -----------------------------
# Sync with base (rebase safety)
# -----------------------------
echo "🔄 Rebasing on $REMOTE/$BASE_BRANCH..."
git rebase -Xtheirs "$REMOTE/$BASE_BRANCH" --quiet || {
    echo "❌ Rebase failed. Resolve conflicts manually."
    exit 1
}

# -----------------------------
# Validate Conventional Commits
# -----------------------------
echo "🔍 Checking for Conventional Commits..."
# Checks if at least one commit in the PR follows conventional formats (feat, fix, chore, docs, etc.)
if ! git log --pretty=format:"%s" "$REMOTE/$BASE_BRANCH"..HEAD | grep -qE "^(feat|fix|chore|refactor|docs|ci|style|test|revert|perf|build|format|deps|sec)(\([a-zA-Z0-9_-]+\))?: "; then
    echo "⚠️ Warning: No commits follow the Conventional Commit format."
    echo "    (e.g., 'feat: add new feature' or 'fix: resolve bug')."
    echo "    This may break automated CHANGELOG generation via tbump."
    read -p "    Do you want to continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo "✅ Commit history looks good."

# -----------------------------
# Validate Packaging Files (Structure only)
# -----------------------------
SPEC_TEMPLATE=$(find rpm -name "*.spec.in" | head -n 1 || true)
if [[ -z "$SPEC_TEMPLATE" ]]; then
    echo "❌ RPM spec template (*.spec.in) not found"
    exit 1
fi
echo "✅ RPM spec template is valid"

if [ ! -f "debian/control" ]; then
    echo "❌ debian/control is missing. PR blocked."
    exit 1
fi
echo "✅ Debian packaging skeleton is present"

if [[ ! -f "scripts/build/update-package-metadata.py" ]]; then
    echo "❌ scripts/build/update-package-metadata.py is missing. PR blocked."
    exit 1
fi
echo "✅ Metadata generator script found"

# -----------------------------
# Commit analysis for PR body
# -----------------------------
if [[ -z "$PR_TITLE" ]]; then
    echo "📝 Generating PR title from commits..."
    PR_TITLE=$(git log --pretty=format:"%s" "$REMOTE/$BASE_BRANCH"..HEAD | head -n 1 | awk -F '\\\\n' '{print $1}')
fi

if [[ -z "$PR_BODY" ]]; then
    echo "📝 Generating PR body from commits..."
    PR_BODY=$(git log --pretty=format:"- %s" "$REMOTE/$BASE_BRANCH"..HEAD)
fi

PR_BODY_FULL="## Target Milestone
v$VERSION

## Changes
$PR_BODY"

# -----------------------------
# Push branch
# -----------------------------
echo "🚀 Pushing branch to $REMOTE..."
git push -u "$REMOTE" "$TARGET_BRANCH" --quiet || {
    echo "❌ Failed to push branch to $REMOTE."
    exit 1
}

# -----------------------------
# Create PR
# -----------------------------
CMD=(gh pr create
    --base "$BASE_BRANCH"
    --head "$TARGET_BRANCH"
    --title "${PR_TITLE}"
    --body "$PR_BODY_FULL"
)

if [[ -n "$REVIEWERS" ]]; then
    CMD+=(--reviewer "$REVIEWERS")
fi

echo "📬 Creating Pull Request..."
"${CMD[@]}" || {
    echo "❌ Failed to create Pull Request."
    exit 1
}

echo "✅ GitOps PR created successfully."
exit 0
