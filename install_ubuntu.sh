#!/usr/bin/env bash
# ============================================================================
# Instalador Automático de Pixeloide Studio Server para Ubuntu / Debian VPS
# ============================================================================
set -e

echo "=== PIXELOIDE STUDIOS · INSTALADOR DE SERVIDOR ==="
sudo apt-get update
sudo apt-get install -y python3 python3-venv python3-pip ffmpeg

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$APP_DIR"

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "[!] Se creó el archivo .env a partir de .env.example (puedes configurar tus API Keys desde la Web UI)."
fi

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

SERVICE_FILE="/etc/systemd/system/pixeloide-studio.service"
echo "Configurando servicio systemd en $SERVICE_FILE ..."
sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Pixeloide Studio Server (16-Bit Documentary Engine)
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable pixeloide-studio
sudo systemctl restart pixeloide-studio

echo ""
echo "✅ Pixeloide Studio Server está corriendo en: http://$(hostname -I | awk '{print $1}'):8080"
echo "   Para ver logs en vivo: sudo journalctl -u pixeloide-studio -f"
