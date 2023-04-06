import asyncio
import logging


async def echo_server(reader, writer):
    try:
        while True:
            data = await reader.read(100)
            if not data:
                break
            writer.write(data)
            await writer.drain()
        writer.close()
    except Exception as e:
        print(e)

async def run(host="", port=3000):
    server = await asyncio.start_server(echo_server, host, port)
    print("YES!")
    logging.info("YES!")
    await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(run())