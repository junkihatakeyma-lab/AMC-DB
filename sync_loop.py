import time
import subprocess
import os
import sys

def main():
    print("Starting periodic sync loop for PartsSearchDB...")
    # interval in seconds (5 minutes)
    interval = 300
    
    while True:
        try:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running import_data.py...")
            subprocess.run([sys.executable, "import_data.py"], check=True)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Sync complete. Waiting {interval} seconds...")
        except subprocess.CalledProcessError as e:
            print(f"Error running sync: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            
        time.sleep(interval)

if __name__ == "__main__":
    main()
