This application polls bus data from the ridecenter.org API and logs bus positions and their arrivals at stops. It also serves the latest bus position data in JSON format at the path `/`. When an arrival occurs, it is logged to the console as well as the database.

# Database setup

You need to initialize the database with recent GTFS data before running. For CET, you can go to [this URL](https://transitfeeds.com/p/cascades-east-transit/440) to download an archive of GTFS data represented in CSV format. You can then import the CSV files into an SQLite database using the `.import` command.

# Python dependencies

This application is intended to be run with python 3.7. You need to have the following python packages installed:
- flask
- bs4

You can install these packages by running:
```
$ pip3 install flask
$ pip3 install bs4
```

You also need to install the `cet_bus` package included in the repo. You can do that by running these two commands in your shell:
```
$ cd cet_bus
$ pip3 install .
```

Alternatively, if you have nix installed, you can simply run `nix-shell shell.nix` to enter a shell with all required packages installed.

# Running

You have to specify the mode (debug or production) and database file via environment variables like this:

```
$ export CET_BUS_MODEL_MODE=DEBUG
$ export CET_BUS_MODEL_DB=arrivals.db   # Same database that contains the gtfs data
```

You can run the application with `flask run -p PORT`, where `PORT` is the port on which you want the application to serve HTTP requests.
