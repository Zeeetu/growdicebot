from fake_useragent import UserAgent
from bson import encode, decode
from time import strftime
import websockets
import asyncio


class GrowDiceBot:
    def __init__(self, sessionid, log_chat=False, log_system=False):
        self.log_system = log_system
        self.sessionid = sessionid
        self.log_chat = log_chat
        self.ws = None

        self.chatState = None
        self.userData = None

        self.userHasJoinedChatRain = False
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
            "chatrainparticipants",
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
        self.userHasJoinedChatRain = True

    async def __handle_state(self):
        self.username = self.userData["data"]["username"]
        self.balance = self.userData["data"]["balance"]
        self.chatRainIsActive = self.chatState["chatRainActive"]
        self.userHasJoinedChatRain = self.userData["data"]["joinedChatRain"]
        print(
            f"Username: {self.username} | Balance: {self.balance} | Chat Rain active: {self.chatRainIsActive} | Chat Rain joined: {self.userHasJoinedChatRain} | Logging chat: {self.log_chat} | Logging system: {self.log_system}"
        )
        if self.chatRainIsActive:
            if not self.userHasJoinedChatRain:
                print(f"Chat Rain is active, joining..")
                await self.__join_chatrain()

    async def __handle(self, msg):
        time = f'[{strftime("%H:%M:%S")}]'
        msg = decode(msg)
        if any(filtered in msg["ID"].lower() for filtered in self.msgfilter):
            pass
        elif msg["ID"] == "useSession":
            print(f"{time} Logged in!" if msg["success"] else "Login failed!")
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
                print(f"{time} [CHAT] {sender}: {text}")
            if sender == "SYSTEM":
                if self.log_system:
                    print(f"{time} [SYSTEM]: {text}")
        elif msg["ID"] == "chatRainFinished":
            print(f"{time} Chat rain finished!")
            self.hasJoinedChatRain = False
        elif msg["ID"] == "chatRainStarted":
            print(f"{time} Chat Rain began, joining..")
            if not self.userHasJoinedChatRain:
                await self.__join_chatrain()
        elif msg["ID"] == "joinChatRain":
            if msg["success"]:
                print(f"{time} Joined chat rain!")
        else:
            print(msg)

    def run(self):
        asyncio.run(self.__connect())
