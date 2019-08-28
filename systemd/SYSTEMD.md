I had luck using Systemd with the following configuration:

1) Moving the provided bitcoin-monitor.service file to /lib/systemd/system/

2) Placing the provided start.sh file in my home directory and making executable

3) Running:

sudo systemctl start bitcoin-monitor
sudo systemctl enable bitcoin-monitor


Be sure to edit the files to use the correct paths for your system.
