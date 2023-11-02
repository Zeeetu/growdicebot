# growdicebot

automatically joins chat rains on growdice.net

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
growdicebot <sessionid> (required) -c or --chat (optional, logs chat) -s or --system (optional, logs system messages)
```

you can also use it in a python script

```python
from growdicebot import GrowDiceBot
bot = GrowDiceBot("your-session-id-here", log_system = True)
bot.run()
```

## how to get session id?

extract sessionIDfrom local storage after logging in on growdice.net on your browser

sessionID will look like this: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

## roadmap / todo

- multiple accounts

- auto-tip to main account

- randomize join time
