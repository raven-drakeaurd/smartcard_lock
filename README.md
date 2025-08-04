Smartcard Lock is a simple program written for my laptop that locks (and unlocks) my computer based on the wether a card is inserted to the smartcard reader. Note: The card does not have to be a smartcard, just any sort of card that fits in the smartcard form factor.

When the program is started, it will ask you for the password for your page. This stores your password temporarily in memory, but not on disk. This helps prevent someone from grabbing the file and getting your password, but still automatically unlocks your computer when the card is inserted.

Dependences:
	zenity (For creating a dialogue to ask you your password)
	xdotool (For sending you password when card is inserted)
	opensc (For reading cards)

To start automatically and run in the background at user login using a systemd user service.
1. Move Your Script to a Safe Location

I prefer ~/.local/bin/:

mkdir -p ~/.local/bin
mv smartcard_lock.py ~/.local/bin/
chmod +x ~/.local/bin/smartcard_lock.py

2. Create a systemd User Service File

Create the directory (if it doesn’t exist):

mkdir -p ~/.config/systemd/user

Then create the service file:

nano ~/.config/systemd/user/smartcard-lock.service

Paste this in:

[Unit]
Description=Smartcard Presence Monitor for Auto Lock/Unlock
After=graphical-session.target

[Service]
Type=simple
ExecStart=%h/.local/bin/smartcard_lock.py
Restart=always
RestartSec=5
Environment=DISPLAY=:0
Environment=XAUTHORITY=%h/.Xauthority

[Install]
WantedBy=default.target

    If you're using Wayland, replace the DISPLAY and XAUTHORITY lines with:

    Environment=WAYLAND_DISPLAY=wayland-0

3. Enable and Start the Service

Reload systemd and enable the service for your user session:

systemctl --user daemon-reexec
systemctl --user daemon-reload
systemctl --user enable smartcard-lock.service
systemctl --user start smartcard-lock.service

4. Enable User Services at Boot

If not already done, you need to enable lingering so your user’s systemd services can run at login:

loginctl enable-linger $USER

You only need to do this once per user.
5. Check Status

Check that it’s running:

systemctl --user status smartcard-lock.service

Check logs if it fails:

journalctl --user-unit=smartcard-lock.service --follow
