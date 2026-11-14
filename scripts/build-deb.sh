#!/usr/bin/env bash
set -euo pipefail

VERSION="${VERSION:-0.2.0}"
ARCH="${ARCH:-amd64}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUILD="$ROOT/build"
STAGE="$BUILD/stage"
WHEELS="$ROOT/packaging/wheels"

# Requires: python3 (>=3.11), python3-venv, python3-dev, python3-pip,
#           nodejs, npm, dpkg-dev, build-essential.
# Build in a Debian 12 container so wheels match the target's ABI.

echo "==> Clean"
rm -rf "$BUILD" "$WHEELS"
mkdir -p "$STAGE"/{DEBIAN,opt/cattendock/{backend,catalog,wheels},etc/cattendock,lib/systemd/system,usr/bin} "$WHEELS"

echo "==> Frontend"
(cd "$ROOT/frontend" && npm ci && npm run build)

echo "==> Python wheels"
pip3 wheel -w "$WHEELS" -r "$ROOT/backend/requirements.txt" >/dev/null

echo "==> Staging"
cp -r "$ROOT/backend/app"            "$STAGE/opt/cattendock/backend/"
cp    "$ROOT/backend/requirements.txt" "$STAGE/opt/cattendock/backend/"
cp -r "$ROOT/frontend/dist"           "$STAGE/opt/cattendock/backend/app/static"
cp -r "$ROOT/catalog/."               "$STAGE/opt/cattendock/catalog/"
cp    "$WHEELS"/*.whl                 "$STAGE/opt/cattendock/wheels/"

cp "$ROOT/packaging/cattendock.service" "$STAGE/lib/systemd/system/"
cp "$ROOT/packaging/cattendock.env"     "$STAGE/etc/cattendock/"
cp "$ROOT/packaging/cattendock"         "$STAGE/usr/bin/"

echo "==> DEBIAN metadata"
cp "$ROOT/packaging/control"  "$STAGE/DEBIAN/"
cp "$ROOT/packaging/postinst" "$STAGE/DEBIAN/"
cp "$ROOT/packaging/prerm"    "$STAGE/DEBIAN/"
cp "$ROOT/packaging/postrm"   "$STAGE/DEBIAN/"
cp "$ROOT/packaging/conffiles" "$STAGE/DEBIAN/"

SIZE_KB=$(du -sk "$STAGE/opt" | cut -f1)
sed -i "s/@VERSION@/$VERSION/g; s/@ARCH@/$ARCH/g; s/@SIZE@/$SIZE_KB/g" "$STAGE/DEBIAN/control"

chmod 0644 "$STAGE/DEBIAN/"{control,prerm,postrm,conffiles}
chmod 0755 "$STAGE/DEBIAN/postinst" "$STAGE/usr/bin/cattendock"

find "$STAGE/opt" -type d -exec chmod 0755 {} \;
find "$STAGE/opt" -type f -exec chmod 0644 {} \;

echo "==> Building"
OUT="$BUILD/cattendock_${VERSION}_${ARCH}.deb"
dpkg-deb --build --root-owner-group "$STAGE" "$OUT" >/dev/null

echo "==> Done: $OUT ($(du -h "$OUT" | cut -f1))"
