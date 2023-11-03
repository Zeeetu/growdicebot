from fake_useragent import UserAgent
from bson import encode, decode
from time import time, strftime
import websockets
import asyncio

from .color import COL


class GrowDiceBot:
    def __init__(self, sessionid, log_chat=False, log_system=False, debug=False):
        self.sessionid = sessionid
        self.ws = None

        self.log_system = log_system
        self.log_chat = log_chat
        self.debug = debug

        self.chatState = None
        self.userData = None

        self.userHasJoinedChatRain = False
        self.chatRainParticipants = None
        self.chatRainIsActive = False

        self.username = None
        self.balance = None

        self.msgfilter = [
            "onlinecount",
            "gamestarting",
            "gamestarted",
            "gameplayerbet",
            "gamefinished",
            "newbets",
            "casesgame",
            "bethistory",
            "gamestate",
            "playercashedout",
        ]

        self.ua = UserAgent()

    async def __connect(self):
        url = "wss://ws.growdice.net/"

        headers = {"User-Agent": self.ua.chrome}

        async with websockets.connect(url, extra_headers=headers) as ws:
            self.ws = ws
            await self.__login()
            while True:
                msg = await ws.recv()
                await self.__handle(msg)

    async def __login(self):
        login_msg = encode({"ID": "useSession", "sessionID": self.sessionid})
        await self.ws.send(login_msg)

    async def __join_chatrain(self):
        join_msg = encode({"ID": "joinChatRain"})
        await self.ws.send(join_msg)

    async def __handle_state(self):
        self.username = self.userData["data"]["username"]
        self.balance = self.userData["data"]["balance"]
        self.chatRainIsActive = self.chatState["chatRainActive"]
        self.userHasJoinedChatRain = self.userData["data"]["joinedChatRain"]
        if self.chatRainIsActive:
            self.chatRainParticipants = self.chatState["chatRainParticipants"]
            self.chatRainEndsIn = int(self.chatState["chatRainTime"] / 1000 - time())
        self.__print_info()
        if self.chatRainIsActive:
            if not self.userHasJoinedChatRain:
                await self.__join_chatrain()

    async def __handle(self, msg):
        msg = decode(msg)
        if any(filtered in msg["ID"].lower() for filtered in self.msgfilter):
            pass
        elif msg["ID"] == "useSession":
            if msg["success"]:
                self.tprint(f"{COL.G}Logged in!{COL.X}")
            else:
                self.tprint(f"{COL.R}Login failed!{COL.X}")
                quit()
        elif msg["ID"] == "userData":
            self.userData = msg
            await self.__handle_state()
        elif msg["ID"] == "chatState":
            self.chatState = msg
        elif msg["ID"] == "chatMessage":
            chatmsg = msg["message"]
            sender = chatmsg["username"]
            text = chatmsg["text"]
            if self.log_chat and sender != "SYSTEM":
                self.tprint(f"[CHAT] {sender}: {text}")
            if sender == "SYSTEM":
                if self.log_system:
                    self.tprint(f"[SYSTEM]: {text}")
        elif msg["ID"] == "chatRainFinished":
            odds = self.__get_odds()
            self.tprint(f"Chat rain finished! [Odds were {odds}%]")
            self.userHasJoinedChatRain = False
        elif msg["ID"] == "chatRainStarted":
            if not self.userHasJoinedChatRain:
                await self.__join_chatrain()
        elif msg["ID"] == "joinChatRain":
            if msg["success"]:
                self.userHasJoinedChatRain = True
                self.tprint(f"{COL.G}Joined{COL.X} Chat Rain!")
            else:
                self.tprint(f"{COL.R}Failed to join{COL.X} Chat Rain!")
        elif msg["ID"] == "chatRainReward":
            reward = msg["reward"]
            self.tprint(f"Won {COL.G}{reward} WLs{COL.X} from Chat Rain!")
        elif msg["ID"] == "chatRainParticipants":
            participants = msg["participants"]
            self.chatRainParticipants = participants
        else:
            if self.debug:
                print(msg)

    def __get_odds(self):
        odds = (5 / self.chatRainParticipants) * 100
        return round(odds, 2)

    def __print_info(self):
        info = f"""
    Username: {COL.Y}{self.username}{COL.X}
    Balance: {COL.Y}{self.balance}{COL.X}
    {f"Chat Rain {COL.G}is active{COL.X}! [Ends in {self.chatRainEndsIn} seconds] [{self.chatRainParticipants} participants]" if self.chatRainIsActive else f"Chat Rain {COL.R}is not active{COL.X}!"}
    {f"Chat Rain {COL.G}joined{COL.X}!" if self.userHasJoinedChatRain else f"Chat Rain {COL.R}not joined{COL.X}!"}
    """
        print(info)

    def tprint(self, content):
        time = f'[{strftime("%H:%M:%S")}]'
        print(f"{COL.B}{time}{COL.X} {content}")

    def run(self):
        asyncio.run(self.__connect())
