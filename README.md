# A Bad General Discord Bot
![test-code](https://github.com/vivax3794/ABGDB/workflows/test-code/badge.svg)

this is a bad bot, don't use it.
unless you are me.

## invite bot
you can invite the bot with [this link](https://discord.com/api/oauth2/authorize?client_id=723933097997107260&permissions=8&scope=bot), idk why the hell you would want this bot tho?!
it is not hosted anywhere and is only online when I am working on it, so like **dont** invite it. it wont be useful.


## run bot locally 
you need [pipenv](https://pypi.org/project/pipenv/) to run this bot.
clone the repo and setup the env:
```bash
git clone https://github.com/vivax3794/ABGDB
cd ABGDB
pipenv sync
```

then make a `.env` file with your discord token like this: ```
TOKEN="your token here"
```

and then you are ready to run the bot!
```bash
pipenv run bot
```

### running tests
want to make sure the bot is working?

simply run the tests:
```bash
pipenv run test
```

## TODO list
you can find my [trello board here](https://trello.com/b/m67oWJxC/abgdb)
