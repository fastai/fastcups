#pip install -r requirements.txt

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
