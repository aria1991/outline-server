import subprocess
import json
import os

def add_bbr(server_name):
    # Check if the Outline server is running
    status = subprocess.run(["outline-manager", "status", server_name], stdout=subprocess.PIPE)
    if "not running" in status.stdout.decode():
        print(f"Error: Outline server '{server_name}' is not running")
        return

    # Stop the Outline server
    subprocess.run(["outline-manager", "stop", server_name])

    # Read the Outline server config
    with open("/etc/outline/config.json", "r") as f:
        config = json.load(f)

    # Enable BBR in the config
    config["congestionControl"] = "bbr"

    # Write the modified config to the file
    with open("/etc/outline/config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Restart the Outline server
    subprocess.run(["outline-manager", "start", server_name])

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Add BBR congestion control to an Outline server")
    parser.add_argument("server_name", help="Name of the Outline server")
    args = parser.parse_args()

    # Check if the Outline manager is installed
    if not os.path.exists("/usr/local/bin/outline-manager"):
        print("Error: Outline manager is not installed")
        exit(1)

    add_bbr(args.server_name)
