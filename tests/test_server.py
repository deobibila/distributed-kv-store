
import asyncio
import unittest

from keyvault.server import KeyValueServer


class TestKeyValueServer(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.app = KeyValueServer()
        self.server = await asyncio.start_server(
            self.app.handle_client, "127.0.0.1", 0
        )
        self.port = self.server.sockets[0].getsockname()[1]

    async def asyncTearDown(self):
        self.server.close()
        await self.server.wait_closed()

    async def send(self, command):
        reader, writer = await asyncio.open_connection(
            "127.0.0.1", self.port
        )
        try:
            writer.write((command + "\n").encode())
            await writer.drain()
            return (await reader.readline()).decode().strip()
        finally:
            writer.close()
            await writer.wait_closed()

    async def test_commands(self):
        self.assertEqual(await self.send("SET name Deo"), "OK")
        self.assertEqual(await self.send("GET name"), "VALUE Deo")
        self.assertEqual(await self.send("EXISTS name"), "1")
        self.assertEqual(await self.send("COUNT"), "1")
        self.assertEqual(await self.send("DELETE name"), "1")
        self.assertEqual(await self.send("GET name"), "NOT_FOUND")

    async def test_concurrent_clients(self):
        commands = [f"SET key{i} value{i}" for i in range(100)]
        results = await asyncio.gather(
            *(self.send(command) for command in commands)
        )
        self.assertEqual(results, ["OK"] * 100)
        self.assertEqual(self.app.store.count(), 100)


if __name__ == "__main__":
    unittest.main()
