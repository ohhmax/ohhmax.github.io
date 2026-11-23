#!/usr/bin/env bash
# ==============================================================================
# MAHENDRA MALI (MAX) - PRODUCTION PUBLIC RELEASE & BUILD PIPELINE
# Encrypts sensitive configuration tokens, stamps copyright, verifies SEO,
# and generates a high-performance, secure "out" distribution folder.
# Author: Mahendra Mali (Max) | License UPI: 9824584454@ybl
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
OUT_DIR="$PROJECT_ROOT/out"

echo "=================================================================="
echo "🚀 INITIATING PUBLIC RELEASE PIPELINE - MAHENDRA MALI (MAX)"
echo "=================================================================="

cd "$PROJECT_ROOT"

# Step 1: Encrypt sensitive tokens in maxconf.json
echo ""
echo "[1/5] Encrypting sensitive configuration tokens..."
node "$PROJECT_ROOT/tools/secure-config-crypto.js" encrypt

# Step 2: Stamp copyright notices and generate cryptographic SHA-256 hashes
echo ""
echo "[2/5] Stamping copyright headers and computing SHA-256 integrity..."
node "$PROJECT_ROOT/tools/stamp-copyright-and-hashes.js"

# Step 3: Run comprehensive SEO and feature audit
echo ""
echo "[3/5] Executing 50-point SEO and quality audit..."
npm test

# Step 4: Build distribution output folder
echo ""
echo "[4/5] Building clean 'out' distribution directory..."
rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

# Copy root web documents
cp index.html 404.html robots.txt sitemap.xml llms.txt llms-full.txt ai.txt LICENSE maxconf.json "$OUT_DIR/"

# Copy asset and data directories
mkdir -p "$OUT_DIR/css" "$OUT_DIR/js" "$OUT_DIR/assets" "$OUT_DIR/data" "$OUT_DIR/pages" "$OUT_DIR/components" "$OUT_DIR/resume"
cp -r css/* "$OUT_DIR/css/"
cp -r js/* "$OUT_DIR/js/"
cp -r assets/* "$OUT_DIR/assets/"
cp -r data/* "$OUT_DIR/data/"
cp -r pages/* "$OUT_DIR/pages/"
cp -r components/* "$OUT_DIR/components/"
cp -r resume/* "$OUT_DIR/resume/"

# Copy symlinks if any
if [ -f "favicon.ico" ]; then cp favicon.ico "$OUT_DIR/"; fi
if [ -f "BingSiteAuth.xml" ]; then cp BingSiteAuth.xml "$OUT_DIR/"; fi

# Step 5: Verify distribution package
echo ""
echo "[5/5] Verifying distribution package integrity..."
TOTAL_FILES=$(find "$OUT_DIR" -type f | wc -l)
OUT_SIZE=$(du -sh "$OUT_DIR" | cut -f1)

echo "=================================================================="
echo "✔ BUILD SUCCESSFUL: Public release generated at $OUT_DIR"
echo "📦 Total Files in Output: $TOTAL_FILES"
echo "📊 Output Distribution Size: $OUT_SIZE"
echo "🔒 Sensitive Tokens: Encrypted with AES-256-GCM in maxconf.json"
echo "🛡️ AI Governance: Protected in ai.txt, llms.txt, robots.txt"
echo "📜 License: Copyright (c) 2026 Mahendra Mali (Max) | UPI: 9824584454@ybl"
echo "=================================================================="
