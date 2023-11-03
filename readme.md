# growdicebot

automatically joins chat rains on growdice.net (growtopia betting site)

## installation

clone package

```bash
  git clone https://github.com/Zeeetu/growdicebot
```

enter directory

```bash
  cd growdicebot
```

install with pip

```bash
  pip install -U .
```

## usage / examples

easiest way to use this is with the cli

```sh
growdicebot <sessionid>
```

view the arguments with

```sh
growdicebot -h
```

you can also use it in a python script

```python
from growdicebot import GrowDiceBot
bot = GrowDiceBot("your-session-id-here", log_system = True)
bot.run()
```

## how to get session id?

extract "sessionID" key from local storage after logging in on growdice.net on your browser

sessionID will look like this: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (uuid)

## roadmap / todo

- multiple accounts

- auto-tip to main account

- randomize join time
