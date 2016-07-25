# Bowling App
Simple bowling scoring application built using Python, Flask, and MongoDB.

## Installation
You'll need the following tools to run the application:

- [Virtual Box](https://www.virtualbox.org/)
- [Vagrant](https://www.vagrantup.com/downloads.html)
- [ChefDK](https://downloads.chef.io/chef-dk/)

After installing the above dependencies:

1. Clone down the repo
2. Navigate to the project root directory in a terminal
3. Run command `vagrant up`

## Usage
The application is RESTful and can be reached from any RESTful client.  Once vagrant is complete the following endpoints can be reached at `http://localhost:7878`:

- `GET 'http://localhost:7878/'` shows application status
- `GET 'http://localhost:7878/games'` retrieves a list of all games
- `POST 'http://localhost:7878/games'` creates a new game with new players formatted in the following:
```json
[
    "First Last",
    "First Last"
]
```
- `GET 'http://localhost:7878/games/:game_id'`retrieves detailed information about a game with the given game_id
- `PUT 'http://localhost:7878/games/:game_id'` sends the roll to the next player's turn.  Format roll as simple text (integer between 0 and 10):
```
10
```
- `DELETE 'http://localhost:7878/games/:game_id'` deactivates a game unless the body of the request contains a valid player id, then that player is deactivated.  Format is simple text (an integer 1 - 4):
```
:player_id
```

Endpoints can be reached through any RESTful client or using an API such as cURL.  A POSTMAN collection has been supplied as well though.

> To turn off the server either stop the vagrant box using one of it's commands such as `vagrant halt` or `vagrant destroy`.  Or SSH in to the vagrant box using `vagrant ssh` and run command `supervisorctl stop all` as root user.

## Testing
There is an accompanying test suite which seeds the database with game information and runs behavior testing.

1. SSH into vagrant machine by using `vagrant ssh` in project root directory
2. Navigate to the project directory in the vagrant box `/home/mark/BowlApp`
3. Run command `python test.py` to see the results of the tests created

## Contributors

- [Mark Hess](https://github.com/Hessmjr) (2016)
