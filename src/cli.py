import argparse
from client import VideoTranslationClient

def main():
    """
    Main function to run the command-line tool for checking the video translation status.
    Allows the user to pass a custom URL for the translation server.

    This function initializes the client, retrieves the status, and prints the result.
    """
    parser = argparse.ArgumentParser(description='Check video translation status.')
    parser.add_argument('--url', type=str, default="http://localhost:5000", help="Base URL of the translation server")
    args = parser.parse_args()

    client = VideoTranslationClient(base_url=args.url)
    status = client.check_status()

    print(f"Final translation status: {status}")

if __name__ == "__main__":
    main()
