# 🎲 growdicebot

plays roulette with the martingale bet strategy and joins chat rains automatically on growdice.net (growtopia betting)

## ⚙️ installation

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

## 📙 basic usage / examples

easiest way to use this is with the cli:

```
growdicebot <sessionid>
```

view the arguments with:

```
growdicebot -h
```

you can also use it in a python script:

```python
from growdicebot import GrowDiceBot
bot = GrowDiceBot("your-session-id-here")
bot.run()
```

## 🃏 how to use martingale system

through cli:

```
growdicebot <sessionid> -mb <amount to bet in WLs> -mc <color to bet on>
```

or in python script:

```python
from growdicebot import GrowDiceBot, RLT #class containing roulette colors
bot = GrowDiceBot("your-session-id-here")
bot.martingale(1, RLT.RED) # betting starts with 1WL on red
```

note: you don't have to call `run()` when using martingale

## 🔎 how to get session id?

extract sessionID from local storage after logging in on growdice.net on your browser

sessionID will look like this: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

## 🗺️ roadmap / todo

- multiple accounts

- auto-tip to main account

- play other games with different strategies

## 🏅 contributing

contributions are always welcome. attempt to mostly adhere to the basic structure of the project when adding new features
