#!/usr/bin/env bash
# Configura el VPS de Robin (5.189.141.180) para servir el marketplace
# de Claude Desktop por HTTPS desde https://api.robinlawyer.ai/plugins.git
#
# Requisitos en el VPS:
#   - git instalado
#   - nginx con SSL ya configurado para robinlawyer.ai
#   - fcgiwrap (para git-http-backend bajo nginx)
#
# Lánzalo desde la Mac:
#   ssh -i ~/.ssh/id_jurix_server root@5.189.141.180 'bash -s' < scripts/setup-vps-marketplace.sh
#
# Después, sube el repo:
#   git remote add origin https://api.robinlawyer.ai/plugins.git
#   git push origin main
#
# Y los abogados instalan con:
#   /plugin marketplace add https://api.robinlawyer.ai/plugins.git

set -euo pipefail

REPO_DIR="/var/git/claude-for-spanish-law.git"
WEB_URL_PATH="/plugins.git"

echo "📦 Instalando dependencias..."
apt-get update -qq
apt-get install -y git fcgiwrap nginx-extras

echo "🗂️  Creando repo bare en ${REPO_DIR}..."
mkdir -p "${REPO_DIR}"
cd "${REPO_DIR}"
git init --bare
git config http.receivepack true
git config http.uploadpack true
chown -R www-data:www-data "${REPO_DIR}"

echo "🌐 Configurando nginx..."
cat > /etc/nginx/snippets/git-marketplace.conf <<'EOF'
# Servir claude-for-spanish-law como marketplace Git por HTTP
location ~ ^/plugins\.git(/.*)?$ {
    fastcgi_pass unix:/var/run/fcgiwrap.socket;
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME /usr/lib/git-core/git-http-backend;
    fastcgi_param GIT_HTTP_EXPORT_ALL "";
    fastcgi_param GIT_PROJECT_ROOT /var/git;
    fastcgi_param PATH_INFO $uri;
    fastcgi_param REMOTE_USER $remote_user;
    # Auth opcional. Si quieres dejarlo público (recomendado para distribución),
    # déjalo sin auth_basic. Si quieres restringir a clientes Robin, descomenta:
    # auth_basic "Robin Plugin Marketplace";
    # auth_basic_user_file /etc/nginx/.htpasswd-marketplace;
}

# También servir directamente marketplace.json desde /.well-known/ para
# instalación rápida sin clonar todo
location = /.well-known/claude-marketplace.json {
    root /var/www/robin-marketplace;
    add_header Content-Type application/json;
    add_header Access-Control-Allow-Origin *;
}
EOF

# Inserta el include en el server block HTTPS principal si no está ya
SITE_CONF="/etc/nginx/sites-available/robinlawyer.ai"
if [ -f "${SITE_CONF}" ] && ! grep -q "git-marketplace.conf" "${SITE_CONF}"; then
    sed -i '/server_name.*robinlawyer.ai/a\    include /etc/nginx/snippets/git-marketplace.conf;' "${SITE_CONF}"
fi

echo "🔄 Recargando nginx..."
nginx -t && systemctl reload nginx

echo "▶️  Habilitando fcgiwrap..."
systemctl enable --now fcgiwrap

echo ""
echo "✅ VPS configurado."
echo ""
echo "Próximos pasos desde la Mac:"
echo "  cd /Users/alonsocuspineracarvajal/Downloads/Abogado_v2/claude-for-spanish-law"
echo "  git init"
echo "  git add ."
echo "  git commit -m 'Robin marketplace v1'"
echo "  git remote add origin https://api.robinlawyer.ai/plugins.git"
echo "  git push -u origin main"
echo ""
echo "El abogado instala con:"
echo "  /plugin marketplace add https://api.robinlawyer.ai/plugins.git"
echo "  /plugin install robin@claude-for-spanish-law"
