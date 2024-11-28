import argparse
from client import VideoTranslationClient

def main():
    parser = argparse.ArgumentParser(description='Check video translation status.')
    parser.add_argument('--url', type=str, default="http://localhost:5000", help="Base URL of the translation server")
    args = parser.parse_args()

    client = VideoTranslationClient()
    status = client.check_status()

    print(f"Final translation status: {status}")

if __name__ == "__main__":
    main()
