#!/usr/bin/env python3
"""Send a failure notification email for the Bambu Filament Tracker."""

import subprocess
import sys


def send_via_osascript(subject: str, body: str, recipient: str) -> bool:
    """Send email via macOS Mail.app using AppleScript."""
    script = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{body}", visible:false}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{recipient}"}}
        end tell
        send newMessage
    end tell
    '''
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=30
        )
        return result.returncode == 0
    except Exception:
        return False


def main():
    if len(sys.argv) < 3:
        print("Usage: notify_failure.py <step_number> <error_message>")
        sys.exit(1)

    step = sys.argv[1]
    error = " ".join(sys.argv[2:])
    recipient = "plazman@aol.com"
    subject = "Bambu Tracker Update Failed"
    body = (
        f"The scheduled Bambu Filament Tracker update failed at Step {step}.\\n\\n"
        f"Error:\\n{error}\\n\\n"
        f"Check the script logs for details."
    )

    # Try Mail.app via AppleScript
    if send_via_osascript(subject, body, recipient):
        print(f"Failure notification sent to {recipient}")
    else:
        # Fallback: write to a local log so it's not silently lost
        log_path = "/tmp/bambu_tracker_failure.log"
        with open(log_path, "a") as f:
            from datetime import datetime
            f.write(f"\n--- {datetime.now()} ---\n")
            f.write(f"Step {step} failed: {error}\n")
        print(f"Could not send email. Logged failure to {log_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
