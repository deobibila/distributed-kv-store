
import asyncio

from keyvault.store import KeyValueStore


class KeyValueServer:
    def __init__(self, host="127.0.0.1", port=9000):
        self.host = host
        self.port = port
        self.store = KeyValueStore()

    def execute(self, command: str) -> str:
        parts = command.strip().split(maxsplit=2)

        if not parts:
            return "ERROR Empty command"

        action = parts[0].upper()

        if action == "SET" and len(parts) == 3:
            self.store.set(parts[1], parts[2])
            return "OK"

        if action == "GET" and len(parts) == 2:
            value = self.store.get(parts[1])
            return f"VALUE {value}" if value is not None else "NOT_FOUND"

        if action == "DELETE" and len(parts) == 2:
            return "1" if self.store.delete(parts[1]) else "0"

        if action == "EXISTS" and len(parts) == 2:
            return "1" if self.store.exists(parts[1]) else "0"

        if action == "COUNT" and len(parts) == 1:
            return str(self.store.count())

        return "ERROR Invalid command"

    async def handle_client(self, reader, writer):
        try:
            while True:
                data = await reader.readline()

                if not data:
                    break

                try:
                    command = data.decode("utf-8")
                    response = self.execute(command)
                except UnicodeDecodeError:
                    response = "ERROR Invalid encoding"

                writer.write((response + "\n").encode("utf-8"))
                await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()

    async def start(self):
        server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port,
            limit=65536,
        )

        print(f"Key-value server running on {self.host}:{self.port}")

        async with server:
            await server.serve_forever()
