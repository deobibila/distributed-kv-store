
import asyncio

from keyvault.server import KeyValueServer


async def main():
    server = KeyValueServer()
    await server.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped")
