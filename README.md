# Distributed Key-Value Store

A Python-based key-value database project focused on asynchronous networking, storage systems, and distributed systems fundamentals.

## Current Features

- Asynchronous TCP server built with `asyncio`
- Concurrent client connections
- In-memory key-value storage
- GET, SET, DELETE, EXISTS, and COUNT operations
- Automated unit and integration tests

## Getting Started

Requires Python 3.11+.

Start the server:

```bash
python main.py
```

Run the tests:

```bash
python -m unittest discover -s tests -v
```

The server listens on `127.0.0.1:9000` and accepts newline-delimited text commands.

## Roadmap

- Write-ahead logging and crash recovery
- LRU caching
- Custom binary TCP protocol
- Primary-replica replication
- Performance benchmarking and load testing

## Architecture

The current implementation uses an asynchronous TCP server with a shared in-memory storage engine. Replication and disk persistence are planned for future iterations.