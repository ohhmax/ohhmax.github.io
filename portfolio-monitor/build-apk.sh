#!/usr/bin/env bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Dynamic Android SDK detection (Local Linux Workstation & GitHub Actions CI)
if [ -z "$ANDROID_HOME" ]; then
    if [ -d "/home/max/Android/Sdk" ]; then
        ANDROID_HOME="/home/max/Android/Sdk"
    elif [ -d "$HOME/Android/Sdk" ]; then
        ANDROID_HOME="$HOME/Android/Sdk"
    elif [ -d "/usr/local/lib/android/sdk" ]; then
        ANDROID_HOME="/usr/local/lib/android/sdk"
    fi
fi

if [ -z "$ANDROID_HOME" ] || [ ! -d "$ANDROID_HOME" ]; then
    echo "Error: Android SDK not found. Please set ANDROID_HOME environment variable."
    exit 1
fi

# Locate build-tools
if [ -z "$BUILD_TOOLS" ] || [ ! -d "$BUILD_TOOLS" ]; then
    BUILD_TOOLS=$(ls -1d "$ANDROID_HOME/build-tools"/* 2>/dev/null | sort -V | tail -n 1)
fi

# Locate highest android platform jar
if [ -z "$PLATFORM" ] || [ ! -f "$PLATFORM" ]; then
    LATEST_PLATFORM_DIR=$(ls -1d "$ANDROID_HOME/platforms"/android-* 2>/dev/null | sort -V | tail -n 1)
    PLATFORM="$LATEST_PLATFORM_DIR/android.jar"
fi

echo "Using Android SDK: $ANDROID_HOME"
echo "Using Build-Tools: $BUILD_TOOLS"
echo "Using Platform Jar: $PLATFORM"

echo "=== 1. PREPARING BUILD DIRECTORIES ==="
rm -rf "$PROJECT_DIR/build"
mkdir -p "$PROJECT_DIR/build/compiled_res"
mkdir -p "$PROJECT_DIR/build/gen"
mkdir -p "$PROJECT_DIR/build/obj"
mkdir -p "$PROJECT_DIR/build/bin"

echo "=== 2. COMPILING RESOURCES (aapt2 compile) ==="
"$BUILD_TOOLS/aapt2" compile --dir "$PROJECT_DIR/res" -o "$PROJECT_DIR/build/compiled_res/res.zip"

echo "=== 3. LINKING RESOURCES & GENERATING R.java (aapt2 link) ==="
"$BUILD_TOOLS/aapt2" link \
    -I "$PLATFORM" \
    "$PROJECT_DIR/build/compiled_res/res.zip" \
    --manifest "$PROJECT_DIR/AndroidManifest.xml" \
    --java "$PROJECT_DIR/build/gen" \
    -o "$PROJECT_DIR/build/bin/app-unaligned.apk" \
    --auto-add-overlay

echo "=== 4. COMPILING JAVA SOURCES (javac -source 8 -target 8) ==="
javac -parameters -source 8 -target 8 -Xlint:-options -encoding UTF-8 \
    -cp "$PLATFORM" \
    -d "$PROJECT_DIR/build/obj" \
    $(find "$PROJECT_DIR/build/gen" "$PROJECT_DIR/src" -name "*.java")

echo "=== 5. DEXING BYTECODE (d8) ==="
"$BUILD_TOOLS/d8" \
    --min-api 26 \
    --output "$PROJECT_DIR/build/bin" \
    --lib "$PLATFORM" \
    $(find "$PROJECT_DIR/build/obj" -name "*.class")

echo "=== 6. PACKAGING DEX INTO APK ==="
cd "$PROJECT_DIR/build/bin"
python3 -c "import zipfile; zf = zipfile.ZipFile('app-unaligned.apk', 'a'); zf.write('classes.dex', 'classes.dex'); zf.close()"

echo "=== 7. ALIGNING APK (zipalign) ==="
"$BUILD_TOOLS/zipalign" -v -p 4 app-unaligned.apk app-aligned.apk

echo "=== 8. SIGNING APK (portfolio-monitor.keystore / debug.keystore) ==="
KEYSTORE="$PROJECT_DIR/portfolio-monitor.keystore"
KS_PASS="maxhive2026"
KS_ALIAS="maxhive"

if [ ! -f "$KEYSTORE" ]; then
    KEYSTORE="$PROJECT_DIR/debug.keystore"
    KS_PASS="android"
    KS_ALIAS="androiddebugkey"
    if [ ! -f "$KEYSTORE" ]; then
        keytool -genkeypair -v \
            -keystore "$KEYSTORE" \
            -alias androiddebugkey \
            -keyalg RSA \
            -keysize 2048 \
            -validity 10000 \
            -storepass android \
            -keypass android \
            -dname "CN=Android Debug,O=Android,C=US"
    fi
fi

"$BUILD_TOOLS/apksigner" sign \
    --ks "$KEYSTORE" \
    --ks-pass "pass:$KS_PASS" \
    --key-pass "pass:$KS_PASS" \
    --ks-key-alias "$KS_ALIAS" \
    --out "$PROJECT_DIR/build/bin/MaxHive-Intelligence.apk" \
    "$PROJECT_DIR/build/bin/app-aligned.apk"

# Also copy APK to root of portfolio-monitor for direct download and release access
cp "$PROJECT_DIR/build/bin/MaxHive-Intelligence.apk" "$PROJECT_DIR/MaxHive-Intelligence.apk"

echo ""
echo "=================================================================="
echo "✔ APK COMPILED & SIGNED SUCCESSFULLY!"
echo "📦 Output: $PROJECT_DIR/build/bin/MaxHive-Intelligence.apk"
echo "📦 Direct: $PROJECT_DIR/MaxHive-Intelligence.apk"
echo "📊 APK Size: $(du -sh "$PROJECT_DIR/MaxHive-Intelligence.apk" | cut -f1)"
echo "=================================================================="
