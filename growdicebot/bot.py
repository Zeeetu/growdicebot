from fake_useragent import UserAgent
from bson import encode, decode
from time import time, strftime
import websockets
import asyncio

from .utils import COL, RLT


class GrowDiceBot:
    def __init__(
        self,
        sessionId,
        logChat=False,
        logSystem=False,
        debug=False,
    ):
        self.__sessionId = sessionId
        self.__ws = None

        self.__logSystem = logSystem
        self.__logChat = logChat
        self.__debug = debug

        self.__chatState = None
        self.__userData = None

        self.__userHasJoinedChatRain = False
        self.__chatRainParticipants = None
        self.__chatRainIsActive = False

        self.__userLastBetOn = None

        self.username = None
        self.balance = None

        self.__msgfilter = [
            "onlinecount",
            "gameplayerbet",
            "roulettegamestarted",
            "newbets",
            "casesgame",
            "bethistory",
            "playercashedout",
        ]

        self.__ua = UserAgent()

    async def __connect(self):
        url = "wss://ws.growdice.net/"

        headers = {"User-Agent": self.__ua.chrome}

        async with websockets.connect(url, extra_headers=headers) as ws:
            self.__ws = ws
            await self.__login()
            while True:
                msg = await ws.recv()
                await self.__handle(msg)

    async def __login(self):
        login_msg = encode({"ID": "useSession", "sessionID": self.__sessionId})
        await self.__ws.send(login_msg)

    async def __join_chatrain(self):
        join_msg = encode({"ID": "joinChatRain"})
        await self.__ws.send(join_msg)

    async def __place_bet_roulette(self, amount, color: RLT):
        bet_msg = encode(
            {"ID": "rouletteGamePlaceBet", "bet": int(amount), "color": (color.value)}
        )
        await self.__ws.send(bet_msg)

    async def __martingale(self):
        if not self.__userLastBetOn:
            await self.__place_bet_roulette(
                self.__martingaleBet, self.__martingaleColor
            )
        elif self.__lastWinningColor == self.__userLastBetOn:
            self.__tprint(f"{COL.G}Won{COL.X} on roulette!")
            self.__martingaleBet = self.__martingaleStart
            await self.__place_bet_roulette(
                self.__martingaleBet, self.__martingaleColor
            )
        else:
            self.__tprint(f"{COL.R}Lost{COL.X} on roulette!")
            self.__martingaleBet *= 2
            await self.__place_bet_roulette(
                self.__martingaleBet, self.__martingaleColor
            )

    async def __handle_state(self):
        if self.__userData["data"] == None:
            self.__tprint(
                f"{COL.R}Session not logged in!{COL.X} Please login using your browser first."
            )
            quit()
        else:
            self.__tprint(f"{COL.G}Logged in!{COL.X}")
        self.username = self.__userData["data"]["username"]
        self.balance = self.__userData["data"]["balance"]
        self.__chatRainIsActive = self.__chatState["chatRainActive"]
        self.__userHasJoinedChatRain = self.__userData["data"]["joinedChatRain"]
        if self.__chatRainIsActive:
            self.__chatRainParticipants = self.__chatState["chatRainParticipants"]
            self.__chatRainEndsIn = int(
                self.__chatState["chatRainTime"] / 1000 - time()
            )
        self.__print_info()
        if self.__chatRainIsActive:
            if not self.__userHasJoinedChatRain:
                await self.__join_chatrain()

    async def __handle(self, msg):
        msg = decode(msg)
        if any(filtered in msg["ID"].lower() for filtered in self.__msgfilter):
            pass
        elif msg["ID"] == "useSession":
            if msg["success"]:
                self.__tprint(f"{COL.G}Initialized!{COL.X}")
            else:
                self.__tprint(
                    f"{COL.R}Initialization failed!{COL.X} (Wrong Session ID?)"
                )
                quit()
        elif msg["ID"] == "userData":
            self.__userData = msg
            await self.__handle_state()
        elif msg["ID"] == "chatState":
            self.__chatState = msg
        elif msg["ID"] == "chatMessage":
            chatmsg = msg["message"]
            sender = chatmsg["username"]
            text = chatmsg["text"]
            if self.__logChat and sender != "SYSTEM":
                self.__tprint(f"[CHAT] {sender}: {text}")
            if sender == "SYSTEM":
                if self.__logSystem:
                    self.__tprint(f"[SYSTEM]: {text}")
        elif msg["ID"] == "chatRainFinished":
            odds = self.__get_odds()
            self.__tprint(f"Chat rain finished! [Odds were {odds}%]")
            self.__userHasJoinedChatRain = False
        elif msg["ID"] == "chatRainStarted":
            if not self.__userHasJoinedChatRain:
                await self.__join_chatrain()
        elif msg["ID"] == "joinChatRain":
            if msg["success"]:
                self.__userHasJoinedChatRain = True
                self.__tprint(f"{COL.G}Joined{COL.X} Chat Rain!")
            else:
                self.__tprint(f"{COL.R}Failed to join{COL.X} Chat Rain!")
        elif msg["ID"] == "chatRainReward":
            reward = msg["reward"]
            self.__tprint(f"Won {COL.G}{reward} WLs{COL.X} from Chat Rain!")
        elif msg["ID"] == "chatRainParticipants":
            participants = msg["participants"]
            self.__chatRainParticipants = participants
        elif msg["ID"] == "updateXP":
            self.__tprint(f"{COL.G}XP +{COL.X}")
        elif msg["ID"] == "rouletteGamePlaceBet":
            if msg["success"]:
                amount = msg["bet"]
                color = msg["color"]
                self.__userLastBetOn = color
                self.__tprint(
                    f"{COL.G}Bet{COL.X} {amount} WLs on {RLT(color).name.title()}"
                )
            else:
                self.__tprint(f"{COL.R}Failed to bet{COL.X} (No balance?)")
        elif msg["ID"] == "rouletteGameFinished":
            rouletteNumber = msg["rouletteNumber"]
            self.__lastWinningColor = self.__get_roulette_color(rouletteNumber)
        elif msg["ID"] == "rouletteGameStarting":
            if self.__martingaleStart and self.__martingaleColor:
                await self.__martingale()
        else:
            if self.__debug:
                print(msg)

    def __get_roulette_color(self, num):
        if num == 0:
            return 2
        if num % 2 == 0:
            return 1
        return 3

    def __get_odds(self):
        odds = (5 / self.__chatRainParticipants) * 100
        return round(odds, 2)

    def __print_info(self):
        info = f"""
    Username: {COL.G}{self.username}{COL.X}
    Balance: {COL.C}{self.balance / 100.0}{COL.X} / {COL.Y}{self.balance}{COL.X}
    {f"Chat Rain {COL.G}is active{COL.X}! [Ends in {self.__chatRainEndsIn} seconds] [{self.__chatRainParticipants} participants]" if self.__chatRainIsActive else f"Chat Rain {COL.R}is not active{COL.X}!"}
    {f"Chat Rain {COL.G}joined{COL.X}!" if self.__userHasJoinedChatRain else f"Chat Rain {COL.R}not joined{COL.X}!"}
    """
        print(info)

    def __tprint(self, content):
        time = f'{COL.B}[{COL.X}{strftime("%H:%M:%S")}{COL.B}]{COL.X}'
        print(f"{time} {content}")

    def martingale(self, start, color: RLT):
        self.__martingaleStart = str(start)
        self.__martingaleColor = color
        self.__martingaleBet = self.__martingaleStart
        print(self.__martingaleStart, self.__martingaleColor)
        self.run()

    def run(self):
        asyncio.run(self.__connect())
