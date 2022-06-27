[![CI](https://github.com/david1992121/p2p-simulation/actions/workflows/ci.yml/badge.svg)](https://github.com/david1992121/p2p-simulation/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/david1992121/p2p-simulation/branch/main/graph/badge.svg?token=YGPQWTSMS0)](https://codecov.io/gh/david1992121/p2p-simulation)

# P2P-Simulating Network

The API service for simulating p2p networks with a tree topology.

## Overall

The network has several trees, each of which has nodes.
The connection and disconnection of the node can be simulated by adding and removing nodes from the network using the API.

## Features

The service has the following three endpoints(the idea is to interact with the program using HTTP calls):

1. The first one is where a node can request to join the p2p network. In this step we just
   assign the node to the best-fitting parent (the node with the most free capacity).
2. With the second endpoint, the node can communicate to the service that it is leaving
   the network. In this case, we want to reorder the current node tree (not all the
   network) to build the solution where the tree has the fewest number of depth levels.
3. The last endpoint will reflect the status of the network, returning in a clear format the current topology of the trees.

## Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/david1992121/p2p-simulation

Activate the virtualenv for your project.

Install project dependencies:

    $ pip install -r requirements.txt

You can now run the development server:

    $ fastapi run

Then the uvicorn will be running on `127.0.0.1:8000`.

## How to checkout the API

The whole API documentation can be checked by opening up either of the following URLs.

```
localhost:8000/redoc
localhost:8000/docs
```
