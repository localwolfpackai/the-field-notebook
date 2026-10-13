#!/usr/bin/env bash
# Find stale remote branches, report them, and (separately) delete them.
#
#   scripts/branch-cleanup.sh report [--days 180]       read-only table of every branch
#   scripts/branch-cleanup.sh delete BRANCH...          dry run: print what would happen
#   scripts/branch-cleanup.sh delete --apply BRANCH...  tag unmerged tips, then delete
#
# Delete only takes branch names you pass. It never picks them for you.
# A branch whose tip is not already in main gets a backup tag first:
#   archive/cleanup/YYYYMMDD/<branch>
# Restore a deleted branch:
#   git push origin refs/tags/archive/cleanup/YYYYMMDD/<branch>:refs/heads/<branch>
set -euo pipefail

PROTECTED='^(main|master|develop|HEAD)$|^(release|prod|staging|ci)/'
BASE=origin/main
DAYS=180
STAMP=$(date +%Y%m%d)

cd "$(git rev-parse --show-toplevel)"
REPO=$(gh repo view --json nameWithOwner --jq .nameWithOwner)

days_ago() {
  if date -v -1d +%s >/dev/null 2>&1; then date -v "-$1d" +%s; else date -d "$1 days ago" +%s; fi
}

ci_status() {
  gh api "repos/$REPO/commits/$1/check-runs" --jq \
    '[.check_runs[].conclusion // "pending"] | if length == 0 then "none"
     elif all(. == "success" or . == "skipped" or . == "neutral") then "green"
     elif any(. == "failure" or . == "timed_out" or . == "cancelled") then "failing"
     else "pending" end' 2>/dev/null || echo "unknown"
}

load_prs() {
  PRS=$(mktemp)
  trap 'rm -f "$PRS"' EXIT
  gh pr list --repo "$REPO" --state all --limit 500 \
    --json number,headRefName,headRefOid,state,labels \
    --jq '.[] | "\(.number)\t\(.headRefName)\t\(.headRefOid)\t\(.state)\t\([.labels[].name] | join(",") | if . == "" then "-" else . end)"' > "$PRS"
}

# Prints one line: verdict<TAB>reason
classify() {
  local br=$1 tip=$2 age=$3 threshold=$4 open closed squash
  open=$(awk -F'\t' -v b="$br" '$2 == b && $4 == "OPEN" {print "#"$1}' "$PRS" | head -1)
  if [ -n "$open" ]; then printf 'keep\topen PR %s\n' "$open"; return; fi
  if git merge-base --is-ancestor "$tip" "$BASE"; then printf 'safe\ttip is in main history\n'; return; fi
  squash=$(awk -F'\t' -v t="$tip" '$3 == t && $4 == "MERGED" {print "#"$1}' "$PRS" | head -1)
  if [ -n "$squash" ]; then printf 'safe\tsquash-merged as %s, tag first\n' "$squash"; return; fi
  if ! git cherry "$BASE" "$tip" | grep -q '^+'; then printf 'safe\tevery commit has an equivalent in main\n'; return; fi
  closed=$(awk -F'\t' -v b="$br" '$2 == b && $4 == "CLOSED" {print "#"$1}' "$PRS" | head -1)
  if [ -n "$closed" ]; then printf 'follow-up\tPR %s closed unmerged, unique commits\n' "$closed"; return; fi
  if [ "$age" -lt "$threshold" ]; then printf 'stale\tno PR, older than threshold, unique commits\n'; return; fi
  printf 'keep\tno PR, recent, unique commits\n'
}

report() {
  local threshold ref br tip age date author ahead stat verdict reason pr labels
  threshold=$(days_ago "$DAYS")
  git fetch --all --prune --quiet
  load_prs
  printf 'branch\tlast_commit\tauthor\tpr\tlabels\tahead\tdiff_vs_main\tci\tverdict\treason\n'
  git for-each-ref --sort=committerdate --format='%(refname:short)' refs/remotes/origin |
  while read -r ref; do
    br=${ref#origin/}
    [ "$br" = origin ] && continue
    echo "$br" | grep -Eq "$PROTECTED" && continue
    tip=$(git rev-parse "$ref")
    age=$(git log -1 --format=%ct "$tip")
    date=$(git log -1 --format=%cs "$tip")
    author=$(git log -1 --format=%an "$tip")
    ahead=$(git rev-list --count "$BASE..$tip")
    stat=$(git diff --shortstat "$BASE...$tip" | sed -E 's/ files? changed/f/; s/ insertions?\(\+\)/+/; s/ deletions?\(-\)/-/; s/^ //')
    pr=$(awk -F'\t' -v b="$br" '$2 == b {print "#"$1":"$4}' "$PRS" | head -1)
    labels=$(awk -F'\t' -v b="$br" '$2 == b {print $5}' "$PRS" | head -1)
    IFS=$'\t' read -r verdict reason < <(classify "$br" "$tip" "$age" "$threshold")
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$br" "$date" "$author" "${pr:--}" "${labels:--}" \
      "$ahead" "${stat:-empty}" "$(ci_status "$tip")" "$verdict" "$reason"
  done
}

delete() {
  local apply=0 br tip tag open
  if [ "${1:-}" = "--apply" ]; then apply=1; shift; fi
  [ $# -gt 0 ] || { echo "name at least one branch" >&2; exit 2; }
  git fetch --all --prune --quiet
  load_prs
  for br in "$@"; do
    if echo "$br" | grep -Eq "$PROTECTED"; then echo "SKIP $br: protected"; continue; fi
    if ! tip=$(git rev-parse --verify --quiet "origin/$br"); then echo "SKIP $br: not on origin"; continue; fi
    open=$(awk -F'\t' -v b="$br" '$2 == b && $4 == "OPEN" {print "#"$1}' "$PRS" | head -1)
    if [ -n "$open" ]; then echo "SKIP $br: open PR $open"; continue; fi
    tag=""
    git merge-base --is-ancestor "$tip" "$BASE" || tag="archive/cleanup/$STAMP/$br"
    if [ "$apply" -eq 0 ]; then
      echo "DRY-RUN $br ${tip:0:7}: ${tag:+tag $tag, then }delete"
      continue
    fi
    if [ -n "$tag" ]; then
      git push --quiet origin "$tip:refs/tags/$tag"
      echo "TAGGED $tag -> ${tip:0:7}"
    fi
    git push --quiet origin --delete "$br"
    echo "DELETED $br (was ${tip:0:7})"
  done
}

cmd=${1:-report}
shift || true
case $cmd in
  report)
    if [ "${1:-}" = "--days" ]; then DAYS=$2; fi
    report ;;
  delete) delete "$@" ;;
  *) sed -n '2,12p' "$0"; exit 2 ;;
esac
