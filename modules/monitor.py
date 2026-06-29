from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .hashing import calculate_hash
from .logger import save_event

from datetime import datetime

import os
import time
import getpass
import psutil


class MonitorHandler(FileSystemEventHandler):

    def process_event(self, event_type, filepath):

        filename = os.path.basename(filepath)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Check if file is inside Sensitive folder
        sensitive = "YES" if "Sensitive" in filepath else "NO"

        # Current user
        username = getpass.getuser()

        # Current process
        try:
            process_name = psutil.Process(os.getpid()).name()
        except:
            process_name = "Unknown"

        # Default values
        source_path = filepath
        destination_path = ""

        hash_before = ""
        hash_after = ""
        integrity_status = "UNKNOWN"

        # Calculate hash if file exists
        if os.path.exists(filepath):

            try:
                hash_after = calculate_hash(filepath)
                hash_before = hash_after
                integrity_status = "PASS"

            except:
                integrity_status = "FAILED"

        # Authorization Check
        authorized = "YES"

        if sensitive == "YES":
            authorized = "NO"

        # Final Status
        status = "ALERT" if sensitive == "YES" else "NORMAL"

        # Save into Database
        save_event(
            timestamp,
            event_type,
            filename,
            source_path,
            destination_path,
            username,
            process_name,
            hash_before,
            hash_after,
            integrity_status,
            sensitive,
            authorized,
            status
        )

        # Display Output
        print("=" * 70)
        print("Time        :", timestamp)
        print("Event       :", event_type)
        print("File        :", filename)
        print("Source      :", source_path)
        print("Destination :", destination_path)
        print("User        :", username)
        print("Process     :", process_name)
        print("Sensitive   :", sensitive)
        print("Authorized  :", authorized)
        print("Integrity   :", integrity_status)
        print("Status      :", status)
        print("=" * 70)

    def on_created(self, event):
        if not event.is_directory:
            self.process_event("CREATED", event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.process_event("MODIFIED", event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.process_event("DELETED", event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.process_event("MOVED", event.dest_path)


folder = "monitored_folder"

observer = Observer()

observer.schedule(
    MonitorHandler(),
    folder,
    recursive=True
)

observer.start()

print("=" * 70)
print(" Secure File Transfer Monitoring System Started ")
print("=" * 70)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer.stop()

observer.join()
