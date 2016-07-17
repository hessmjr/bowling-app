# Bowling App
Bowling scoring application for coding challenge with The Zebra.

## Installation
You'll need the following tools to run the application:

- [Virtual Box](https://www.virtualbox.org/)
- [ChefDK](https://downloads.chef.io/chef-dk/mac/)
- [Vagrant](https://www.vagrantup.com/downloads.html)

After installing the above dependencies:

- Clone down the repo
- Navigate to the project directory in a terminal
- Run command `vagrant up`

## Usage
The application is RESTful and can be reached from any RESTful client.  Once vagrant is complete:

## Thoughts
Some of my thoughts on the design of the application:

- Used Python's Flask framework due to its simple nature for quick and easy development
- For persistent storage I utilized MongoDB.  The document store allowed the greatest freedom for data modeling as well as simple deployment and ease of use.
- An RDB like MySQL would be a decent choice too, however adds unnecessary complexity to data model.  Would require a games table, players table, scores table, and join tables which could require a lot more additional setup.
- Also began development with plan to use Redis for easy use and deployment as well as great performance.  However unnecessary database calls would be required due to its key, value nature with no ability for nested objects.

## Contributors

- [Mark Hess](https://github.com/Hessmjr)
