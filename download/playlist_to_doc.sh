#!/usr/bin/env bash
# playlist_to_doc.sh — Merge transcripts, chapters, and descriptions
# Usage:
#   bash playlist_to_doc.sh "<playlist_url>" [--out "Custom-Name.md"]
# Output: Channel-Playlist_Title.md (auto-generated) or custom filename
#
# Notes:
# - Requires: yt-dlp, jq
# - Tested in MSYS2/MinGW bash; paths kept POSIX to avoid Windows quoting pitfalls.
# - Captions: prefers human-uploaded; falls back to auto-generated when needed.

set -euo pipefail

# ---------- args ----------
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"<playlist_url>\" [--out \"Custom-Name.md\"]" >&2
  exit 1
fi

PLAYLIST_URL="$1"; shift || true
OUT_FILE=""  # Will be set after we get playlist info
SUB_LANGS="en"   # English only

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out)  OUT_FILE="$2"; shift 2;;
    *) echo "Unknown arg: $1" >&2; exit 2;;
  esac
done

# ---------- deps ----------
need() { command -v "$1" >/dev/null 2>&1 || { echo "Missing dependency: $1" >&2; exit 3; }; }
need yt-dlp
need jq

# ---------- layout ----------
WORKDIR="$(pwd)/_ytpl_work_$(date +%s)"
mkdir -p "$WORKDIR"

echo "==> Working directory: $WORKDIR"

# Output template: simplified structure for MinGW compatibility
# We do NOT download media; only sidecar files (subs, description, info.json)
OUT_TMPL="$WORKDIR/%(id)s.%(ext)s"

echo "==> Output template: $OUT_TMPL"

echo "==> Fetching metadata, descriptions, and captions …"
yt-dlp \
  --yes-playlist \
  --ignore-errors \
  --skip-download \
  --write-description \
  --write-info-json \
  --write-subs \
  --write-auto-subs \
  --sub-langs "$SUB_LANGS" \
  --sub-format vtt \
  --no-abort-on-error \
  -o "$OUT_TMPL" \
  "$PLAYLIST_URL"

echo "==> yt-dlp completed. Checking working directory contents..."
echo "==> Working directory: $WORKDIR"
ls -la "$WORKDIR" 2>/dev/null || echo "Working directory not accessible"
find "$WORKDIR" -type f 2>/dev/null | head -10 || echo "No files found or directory not accessible"

# ---------- helpers ----------
# Convert WebVTT to plain text with proper sentences and paragraphs
vtt_to_text() {
  # stdin: vtt, stdout: formatted text
  awk '
    BEGIN{ 
      in_note=0; in_style=0; last_line=""
      sentence_buffer=""
      words_in_paragraph=0
    }
    {
      # remove BOM
      gsub(/^\xef\xbb\xbf/,"",$0)
      # enter/exit NOTE or STYLE blocks
      if ($0 ~ /^NOTE(\b|$)/) { in_note=1; next }
      if ($0 ~ /^STYLE(\b|$)/) { in_style=1; next }
      if (in_note && $0 ~ /^$/) { in_note=0; next }
      if (in_style && $0 ~ /^$/) { in_style=0; next }
      if (in_note || in_style) next

      # skip WEBVTT header and metadata markers
      if ($0 ~ /^WEBVTT/) next
      if ($0 ~ /^Kind:/) next
      if ($0 ~ /^Language:/) next

      # skip timestamp lines (cue timings)
      if ($0 ~ /^[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3} *-->/) next
      if ($0 ~ /^[0-9]{1,2}:[0-9]{2}\.[0-9]{3} *-->/) next

      # remove inline timestamps like <00:00:24.000><c>text</c>
      gsub(/<[0-9]{1,2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}><c>/, "")
      gsub(/<\/c>/, "")
      
      # remove any remaining timestamp patterns
      gsub(/[0-9]{1,2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}/, "")
      gsub(/[0-9]{1,2}:[0-9]{2}\.[0-9]{3}/, "")

      # remove [Music] and other cue markers
      gsub(/^\[Music\]$/, "")
      gsub(/^\[.*\]$/, "")

      # process non-empty, non-duplicate lines
      if (NF > 0 && $0 != last_line) {
        # trim whitespace
        gsub(/^[ \t]+/, "", $0)
        gsub(/[ \t]+$/, "", $0)
        
        # add to sentence buffer
        if (sentence_buffer == "") {
          sentence_buffer = $0
        } else {
          sentence_buffer = sentence_buffer " " $0
        }
        
        words_in_paragraph += NF
        
        # check if sentence ends (period, exclamation, question mark)
        if ($0 ~ /[.!?]$/) {
          print sentence_buffer
          sentence_buffer = ""
          
          # start new paragraph every 4-6 sentences or 80-120 words
          if (words_in_paragraph > 80) {
            print ""
            words_in_paragraph = 0
          }
        }
        
        last_line = $0
      }
    }
    END {
      # print any remaining sentence buffer
      if (sentence_buffer != "") {
        print sentence_buffer
      }
    }
  '
}

# Choose best transcript file in a per-video directory.
# Preference: human-uploaded > auto; then prefer requested primary language first if present.
pick_transcript_file() {
  local dir="$1"
  local lang_csv="$2" # e.g., "en,*"
  # Build preferred language order array (comma-separated)
  IFS=',' read -r -a langs <<< "$lang_csv"

  # 1) Try human-uploaded for preferred langs
  for L in "${langs[@]}"; do
    # glob matches like .en.vtt or .en-US.vtt (avoid .auto.vtt)
    shopt -s nullglob
    for f in "$dir"/*.vtt; do
      base="${f##*/}"
      # skip auto variants
      [[ "$base" == *".auto.vtt" ]] && continue
      # if lang label matches prefix (en or en-XX)
      if [[ "$L" == "*" || "$base" == *".${L}.vtt" || "$base" == *".${L}-"*.vtt ]]; then
        echo "$f"; return 0
      fi
    done
    shopt -u nullglob
  done

  # 2) Any human-uploaded VTT
  shopt -s nullglob
  for f in "$dir"/*.vtt; do
    [[ "${f##*/}" == *".auto.vtt" ]] && continue
    echo "$f"; shopt -u nullglob; return 0
  done
  shopt -u nullglob

  # 3) Auto-generated for preferred langs
  for L in "${langs[@]}"; do
    shopt -s nullglob
    for f in "$dir"/*.auto.vtt; do
      base="${f##*/}"
      if [[ "$L" == "*" || "$base" == *".${L}.auto.vtt" || "$base" == *".${L}-"*.auto.vtt ]]; then
        echo "$f"; shopt -u nullglob; return 0
      fi
    done
    shopt -u nullglob
  done

  # 4) Any auto-generated VTT
  shopt -s nullglob
  for f in "$dir"/*.auto.vtt; do
    echo "$f"; shopt -u nullglob; return 0
  done
  shopt -u nullglob

  return 1
}

# Safe read from info.json (prints empty if missing)
jq_get() {
  local key="$1" json="$2"
  jq -r "$key // empty" "$json"
}

# Sanitize filename by removing/replacing problematic characters
sanitize_filename() {
  local name="$1"
  # Remove or replace characters that are problematic in filenames
  echo "$name" | sed 's/[<>:"/\\|?*]/_/g' | sed 's/[[:space:]]\+/_/g' | sed 's/_\+/_/g' | sed 's/^_\|_$//g'
}

# Normalize Windows paths to Unix paths for MinGW compatibility
normalize_path() {
  local path="$1"
  # Convert backslashes to forward slashes and clean up
  echo "$path" | sed 's/\\/\//g' | sed 's/^[A-Z]:\///' | sed 's/^\/c\///'
}

# Search for files using Windows-style paths and convert them
find_windows_files() {
  local workdir="$1"
  local pattern="$2"
  local files=()
  
  # Try to find files with Windows-style paths
  while IFS= read -r -d '' file; do
    # Convert Windows path to Unix path
    unix_path=$(echo "$file" | sed 's/\\/\//g')
    # Remove drive letter prefix if present
    unix_path=$(echo "$unix_path" | sed 's/^[A-Z]:\///')
    # Remove /c/ prefix if present (MinGW style)
    unix_path=$(echo "$unix_path" | sed 's/^\/c\///')
    
    if [[ -f "$unix_path" ]]; then
      files+=("$unix_path")
    fi
  done < <(find "$workdir" -type f -name "$pattern" -print0 2>/dev/null | head -c -1)
  
  echo "${files[@]}"
}

# ---------- merge ----------
# Find all info.json files (each corresponds to one video)
echo "==> Searching for info.json files..."
INFO_FILES=($(find_windows_files "$WORKDIR" "*.info.json"))

# Fallback: try direct find if the above fails
if [[ ${#INFO_FILES[@]} -eq 0 ]]; then
  echo "==> Fallback: direct find search..."
  mapfile -t INFO_FILES < <(find "$WORKDIR" -type f -name "*.info.json" 2>/dev/null | sort)
fi

echo "==> Found ${#INFO_FILES[@]} info.json files"

PL_TITLE=""
PL_CHANNEL=""
if [[ ${#INFO_FILES[@]} -gt 0 ]]; then
  # Use the first JSON to extract playlist and channel info
  first_json="${INFO_FILES[0]}"
  PL_TITLE="$(jq_get '.playlist_title' "$first_json")"
  PL_CHANNEL="$(jq_get '.playlist_uploader' "$first_json")"
  
  # Fallback: if no playlist_uploader, try uploader from individual video
  if [[ -z "$PL_CHANNEL" || "$PL_CHANNEL" == "null" ]]; then
    PL_CHANNEL="$(jq_get '.uploader' "$first_json")"
  fi
fi

# Generate output filename if not specified by user
if [[ -z "$OUT_FILE" ]]; then
  if [[ -n "$PL_CHANNEL" && -n "$PL_TITLE" ]]; then
    # Format: "Channel-Playlist Title.md"
    CLEAN_CHANNEL="$(sanitize_filename "$PL_CHANNEL")"
    CLEAN_TITLE="$(sanitize_filename "$PL_TITLE")"
    OUT_FILE="${CLEAN_CHANNEL}-${CLEAN_TITLE}.md"
  elif [[ -n "$PL_TITLE" ]]; then
    # Fallback: just playlist title
    CLEAN_TITLE="$(sanitize_filename "$PL_TITLE")"
    OUT_FILE="${CLEAN_TITLE}.md"
  else
    # Final fallback: timestamped filename
    OUT_FILE="playlist_merged_$(date +%Y%m%d_%H%M%S).md"
  fi
fi

echo "==> Merging into: $OUT_FILE"
: > "$OUT_FILE"

{
  echo "========================================"
  echo "Playlist: ${PL_TITLE:-(unknown title)}"
  echo "URL     : $PLAYLIST_URL"
  echo "Generated: $(date -Iseconds)"
  echo "========================================"
  echo
} >> "$OUT_FILE"

for J in "${INFO_FILES[@]}"; do
  DIR="$(dirname "$J")"
  VID_ID="$(jq_get '.id' "$J")"
  TITLE="$(jq_get '.title' "$J")"
  UPLOAD_DATE="$(jq_get '.upload_date' "$J")"
  CHANNEL="$(jq_get '.uploader' "$J")"
  WEBURL="$(jq_get '.webpage_url' "$J")"

  echo "Processing: $TITLE [$VID_ID]"

  {
    echo "------------------------------------------------------------"
    echo "Title      : $TITLE"
    [[ -n "$CHANNEL" ]] && echo "Channel    : $CHANNEL"
    [[ -n "$UPLOAD_DATE" ]] && echo "Upload Date: $UPLOAD_DATE"
    [[ -n "$WEBURL" ]] && echo "URL        : $WEBURL"
    echo

    # Description
    DESC_FILE="$DIR/${VID_ID}.description"
    if [[ -f "$DESC_FILE" ]]; then
      echo "### Description"
      echo
      cat "$DESC_FILE"
      echo
    else
      echo "### Description"
      echo
      echo "(No description available)"
      echo
    fi

    # Chapters
    echo "### Chapters"
    CH_COUNT=$(jq -r '.chapters | length // 0' "$J")
    if [[ "$CH_COUNT" -gt 0 ]]; then
      # List: [HH:MM:SS] Chapter Title
      jq -r '.chapters[] | "[" + (.start_time | tonumber | strftime("%T")) + "] " + .title' \
         --argjson now 0 \
         "$J"
    else
      echo "(No chapters found)"
    fi
    echo

    # Transcript
    echo "### Transcript"
    # Look for transcript file matching this specific video ID
    VTT_FILE="$DIR/${VID_ID}.en.vtt"
    if [[ -f "$VTT_FILE" ]]; then
      vtt_to_text < "$VTT_FILE"
    else
      # Fallback to old method if specific file not found
      if TRF="$(pick_transcript_file "$DIR" "$SUB_LANGS")"; then
        vtt_to_text < "$TRF"
      else
        echo "(No captions available)"
      fi
    fi
    echo
  } >> "$OUT_FILE"

done

echo "==> Done."
echo "Merged document: $OUT_FILE"
