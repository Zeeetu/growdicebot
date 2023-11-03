import argparse
from .bot import GrowDiceBot


def main():
    args = parse()
    bot = GrowDiceBot(args.sessionid, args.log_chat, args.log_system, args.debug)
    bot.run()


def parse():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument("sessionid", type=str, help="Session ID (required)")
    ap.add_argument(
        "-c",
        "--chat",
        action="store_true",
        help="Enable chat logging (optional)",
        dest="log_chat",
    )
    ap.add_argument(
        "-s",
        "--system",
        action="store_true",
        help="Enable system logging (optional)",
        dest="log_system",
    )
    ap.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debugging websocket messages (optional)",
        dest="debug",
    )
    return ap.parse_args()


if __name__ == "__main__":
    main()
