# Bowling App
Bowling scoring application.

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

- Endpoint 1

Turn off server by ssh and supervisor off...

## Testing
There is an accompanying test suite which seeds the database with game information and runs behavior testing.

1. SSH into vagrant machine by using `vagrant ssh` in project root directory (if vagrant box is running)
2. ...

## Thoughts
Some of my thoughts on the design of the application:

- Used Python's Flask framework due to its simple nature for quick and easy development (considered Bottle and Django)
- For persistent storage I utilized MongoDB.  The document store allowed the greatest freedom for data modeling as well as simple deployment and ease of use.
- An RDB like MySQL would be a decent choice too, however adds unnecessary complexity to data model.  Would require a games table, players table, scores table, and join tables which could require a lot more additional setup.
- Also began development with plan to use Redis for easy use and deployment as well as great performance.  However unnecessary database calls would be required due to its key, value nature with no ability for nested objects.
- Focused on behavior testing for endpoints instead of unit testing for individual methods due to time constraints and fluid nature of the design

## Contributors

- [Mark Hess](https://github.com/Hessmjr)
