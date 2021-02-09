#!/bin/bash
rm -rf "/opt/dml"
cp -r . "/opt/dml"
dd status=none of=/usr/local/bin/dml << EOF
#!/bin/bash
/opt/dml/main.py \$HOME/Syncthing/Personal/dml
EOF
chmod +x /usr/local/bin/dml
