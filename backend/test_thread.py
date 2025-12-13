import threading
import time
from test_processing import test_process

# Use the same file as before
target = "temp_uploads/70c8b97a-7f48-4cdd-b650-63530fba2a6d_WhatsApp Video 2025-12-11 at 22.43.12.mp4"

def run_in_thread():
    print("Starting thread...")
    test_process(target)
    print("Thread finished.")

if __name__ == "__main__":
    print("Main process started.")
    t = threading.Thread(target=run_in_thread)
    t.start()
    t.join()
    print("Main process finished.")
