import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_to_watch):
        self.file_to_watch = file_to_watch

    def on_modified(self, event):
        # Check if the modified file is the one we are watching
        if event.src_path == self.file_to_watch:
            print(f"File '{self.file_to_watch}' has been modified.")
            # Execute the Python script itself
            try:
                result = subprocess.run(['python', self.file_to_watch], check=True, capture_output=True, text=True)
                print("Output of the script:")
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print("Error executing the script:")
                print(e.stderr)

def watch_and_execute_file(file_to_watch):
    # Set up the event handler
    event_handler = FileChangeHandler(file_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_to_watch) or '.', recursive=False)

    # Start the observer
    observer.start()
    print(f"Started watching '{file_to_watch}' for changes...")

    try:
        while True:
            # Keep the script running
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping the file watcher...")
        observer.stop()

    observer.join()

if __name__ == "__main__":
    # Get the file path of the script itself
    file_to_watch = '/Users/sarveshschauhan/Documents/Atri/creator.py'
    
    watch_and_execute_file(file_to_watch)

    # Example functionality to show execution
    print("This is the script running!")