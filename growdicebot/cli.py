import argparse
from .bot import GrowDiceBot
from .utils import RLT

colors = {"red": RLT.RED, "green": RLT.GREEN, "black": RLT.BLACK}


def main():
    args = parse()
    bot = GrowDiceBot(args.sessionid, args.logChat, args.logSystem, args.debug)
    if args.martingaleBet and args.martingaleColor:
        print(args.martingaleBet, colors[args.martingaleColor.lower()])
        bot.martingale(args.martingaleBet, colors[args.martingaleColor.lower()])
    else:
        bot.run()


def parse():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument("sessionid", type=str, help="Session ID (required)")
    ap.add_argument(
        "-c",
        "--chat",
        action="store_true",
        help="Enable chat logging (optional)",
        dest="logChat",
    )
    ap.add_argument(
        "-s",
        "--system",
        action="store_true",
        help="Enable system logging (optional)",
        dest="logSystem",
    )
    ap.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debugging websocket messages (optional)",
        dest="debug",
    )
    ap.add_argument(
        "-mb",
        "--martingalebet",
        type=int,
        help="Martingale bet (optional)",
        dest="martingaleBet",
    )
    ap.add_argument(
        "-mc",
        "--martingalecolor",
        choices=["red", "green", "black"],
        help="Martingale color (optional)",
        dest="martingaleColor",
    )
    return ap.parse_args()


if __name__ == "__main__":
    main()
