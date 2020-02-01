# Auto Loop

A tool for automating loop in and loop out operations for a node. Auto loop
monitors the state of loop out operations and records them in a database. In
addition, it provides a tool that can run and automatically attempt loop out
operations based on the current status of your channels.

Desired channel states and maximum fees are set in `autoloop/config.py`.

When running in automated mode, Auto Loop will attempt to loop out channels
that meet the specified criteria. Upon failure, it will wait the specified
number of days before trying again. In the future this will be implemented as
an exponential backoff. Every attempt will be stored in a local database.

# Usage

This script needs to run on the same instance as your lnd and loop nodes.

Install Dependencies:

```
pipenv install
./gen_grpc.sh
```

Start the monitor. This records the state of any active loop out operations:

```
pipenv python autoloop/run.py monitor
```

Start the automator. This will being automatically attempting loop out
operations based on your `autoloop/config.py` file:

```
pipenv python autoloop/run.py auto
```
