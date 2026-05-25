#!/usr/bin/env bash
# Publica una nueva versión del marketplace al VPS de Robin.
# Asume que el VPS ya está configurado (ver setup-vps-marketplace.sh).
#
# Uso desde la Mac:
#   ./scripts/publish.sh "1.0.1 — descripcion del cambio"

set -euo pipefail

cd "$(dirname "$0")/.."

if [ -z "${1:-}" ]; then
    echo "Uso: $0 \"mensaje de commit\""
    exit 1
fi

echo "🔍 Validando antes de publicar..."
python3 scripts/validate.py
python3 scripts/lint-tool-scope.py

echo "📦 Commit y push..."
git add .
git commit -m "$1" || echo "  (sin cambios que commit)"
git push origin main

echo ""
echo "✅ Publicado."
echo ""
echo "Sincronizando también el marketplace.json para /.well-known/:"
ssh -i ~/.ssh/id_jurix_server root@5.189.141.180 'mkdir -p /var/www/robin-marketplace/.well-known'
scp -i ~/.ssh/id_jurix_server .claude-plugin/marketplace.json \
    root@5.189.141.180:/var/www/robin-marketplace/.well-known/claude-marketplace.json

echo ""
echo "Los abogados que ya tienen el marketplace añadido recibirán la"
echo "actualización al siguiente /plugin update."
