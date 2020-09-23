# A Bad General Discord Bot
![test-code](https://github.com/vivax3794/ABGDB/workflows/test-code/badge.svg)

this is a bad bot, don't use it.
unless you are me.


## run bot locally 
This bot uses a postgres database, so you need to provide that, the bot will create the needed tables on start
you need [pipenv](https://pypi.org/project/pipenv/) to run this bot.
clone the repo and setup the env:
```bash
git clone https://github.com/vivax3794/ABGDB
cd ABGDB
pipenv sync
```

then make a `.env` file with your secret stuff like this:
```
TOKEN="your token here"
DATABASE_URL="your database url here"
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
