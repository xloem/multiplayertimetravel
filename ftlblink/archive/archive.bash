#!/bin/bash
# modified from generation by chat.mistral.ai
#!/bin/bash
set -euo pipefail

BUNDLES_DIR="."
STATE_FILE="$BUNDLES_DIR/.state"

mkdir -p "$BUNDLES_DIR"

# Get last commit and bundle number
last_line=$(tail -n 1 "$STATE_FILE" 2>/dev/null || echo "00000:0000000000000000000000000000000000000000")
last_num=${last_line%:*}
last_commit=${last_line#*:}
next_num=$((10#$last_num + 1))
next_num_padded=$(printf "%05d" "$next_num")
bundle_file="$BUNDLES_DIR/bundle_$next_num_padded.bundle"

# Create incremental bundle
echo "Creating bundle $next_num_padded (since $last_commit)..."
if [ "$last_commit" = "0000000000000000000000000000000000000000" ]; then
    # First run: bundle everything
    echo "Creating initial full bundle $next_num_padded..."
    git bundle create "$bundle_file" --all
else
    # Incremental bundle
    echo "Creating bundle $next_num_padded (since $last_commit)..."
    git bundle create "$bundle_file" "$last_commit..HEAD" --all
fi

python3 ditem_load.py wallet.json "$bundle_file" > "$bundle_file".json
git add "$bundle_file".json
git commit -m "$bundle_file"

# Update state
echo "$next_num_padded:$(git rev-parse HEAD)" >> "$STATE_FILE"
echo "Done: $bundle_file"

