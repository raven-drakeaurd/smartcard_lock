#!/usr/bin/env python3

import subprocess
import time
import logging
import sys

# === CONFIGURATION ===

CHECK_INTERVAL = 3  # Interval between card checks (in seconds)

LOCK_COMMAND = ["loginctl", "lock-session"]
# Alternatives:
# LOCK_COMMAND = ["gnome-screensaver-command", "--lock"]
# LOCK_COMMAND = ["xdg-screensaver", "lock"]

# === LOGGING SETUP ===

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# === FUNCTION DEFINITIONS ===

def prompt_password():
    """Prompts the user for their password via GUI using zenity."""
    try:
        output = subprocess.check_output(
            ["zenity", "--password", "--title=Smartcard Unlock"],
            text=True
        ).strip()
        logging.info("Password received from user.")
        return output
    except subprocess.CalledProcessError:
        logging.error("Password prompt was canceled or failed.")
        sys.exit(1)

def get_card_present():
    """Returns True if a smart card is present in any reader."""
    try:
        output = subprocess.check_output(
            ["opensc-tool", "-l"], stderr=subprocess.DEVNULL, timeout=2
        )
        return b"Yes" in output
    except subprocess.TimeoutExpired:
        logging.warning("Timeout while checking card presence.")
    except subprocess.CalledProcessError:
        logging.error("opensc-tool failed to run.")
    return False

def lock_screen():
    """Locks the screen using the configured command."""
    try:
        subprocess.run(LOCK_COMMAND, check=True)
        logging.info("Screen locked.")
    except Exception as e:
        logging.error(f"Failed to lock screen: {e}")

def type_password(password):
    """Types the password using xdotool and presses Enter."""
    try:
        subprocess.run(["xdotool", "type", "--delay", "100", password], check=True)
        subprocess.run(["xdotool", "key", "Return"], check=True)
        logging.info("Password typed and Enter pressed.")
    except Exception as e:
        logging.error(f"Failed to type password: {e}")


# === MAIN FUNCTION ===

def main():
    logging.info("Starting smart card monitor...")

    password = prompt_password()
    card_present_last = False

    while True:
        card_present_now = get_card_present()

        if card_present_now:
            if not card_present_last:
                logging.info("Smart card detected.")
                type_password(password)
                card_present_last = True
        else:
            if card_present_last:
                logging.info("Smart card removed. Locking screen...")
                lock_screen()
                card_present_last = False

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

