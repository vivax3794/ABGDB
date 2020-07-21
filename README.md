# A Bad General Discord Bot
![test-code](https://github.com/vivax3794/ABGDB/workflows/test-code/badge.svg)

this is a bad bot, don't use it.
unless you are me.



# run bot locally 
this bot uses python3.8

first clone the repo and cd into it:
```bash
git clone https://github.com/vivax3794/ABGDB
cd ABGDB
```
it is recommended to create virtualenviroment, but that will not be coverd here.

then install the used libs with pip
```bash
pip install -r requirements.txt
```

than add a file call `config_SECRET.py` with these content:
```python
TOKEN = "your bot token"
```
if you dont know were you can get a bot token here is a nice article: <https://www.writebots.com/discord-bot-token/>

now you can run the bot (make sure to run with python3):
```bash
python -m src
```
## running tests
want to make sure the bot is working?

simply run pytest:
```bash
python -m pytest tests/
```

# TODO list
you can find my [trello board here](https://trello.com/b/m67oWJxC/abgdb)
