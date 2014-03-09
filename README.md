# Poltergeist

A competition database interface for [Student Robotics](https://www.studentrobotics.org).

Getting Started
===============

Pre-reqs:

* redis, version 2.6 or later
* redis-py
* docopt
* PyYAML
* python-dateutil (v1.5)
* local submodules
* nose (for testing)
* mock (for testing)

You should install the python related pre-reqs using `./install` (which will
also ensure the submodules are present).
This creates a virtualenv at `dep`, which is used by all the scripts in
the root of the repo.

Since the poltergeist library uses a redis instance as its datastore, a
redis-server needs to be running for poltergeist to do anything useful.

For developing, you can start the redis server using `./start-redis`, and
stop it using `./stop-redis`. Production environments are expected to run
the redis server as a service or similar.

Tests
-----

Run the tests using `./run-tests` in the root. The tests rely on nosetest
setting up the right paths for the tests to magically find the sources,
so even when running just one test case, you still need to run them from
the root.

Interfaces
==========
There is one main interface to compd, which is just a direct socket connection.

The socket connection is available on port 18333 (by default, set by `control_port` in `config.yaml`)
on the host machine. Into this connection, commands can be pumped with a newline as the terminating character.
For instance:
~~~~
echo list-teams | nc localhost 18333
~~~~
Because it sucks to have to pipe things through netcat, there's a wrapper cli
that can be used instead:
~~~~
./command list-teams
~~~~

Credit
======

This is a fork of Alistair Lynn's compd.

With thanks to Rob Spanton, Scarzy, Sam Phippen, Edd Seabrook and Ben Clive
 for ideas and work on the previous iterations of compd.
