pip install -r requirements.txt

ulimit -n 100000

mkdir -p ~/.config/systemd/user/

current_dir=`pwd`

cat <<EOF > ~/.config/systemd/user/fastcups.service
[Unit]
Description=Fastcups Service

[Service]
ExecStart=/usr/bin/python `pwd`/fastcups.py
Environment=PYTHONUNBUFFERED=1
Restart=on-failure

[Install]
WantedBy=default.target
EOF

systemctl --user enable fastcups
sudo loginctl enable-linger $USER

sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo tee /etc/apt/trusted.gpg.d/caddy-stable.asc
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy

sudo tee /etc/caddy/Caddyfile > /dev/null <<EOF
http://199.38.217.21

abort /favicon.ico
reverse_proxy 127.0.0.1:5000
EOF

sudo HOME=~caddy caddy trust
sudo ufw allow https
