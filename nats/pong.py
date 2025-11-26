import asyncio
import argparse
from nats.aio.client import Client as NATS

async def run(server_ip, port):
    url = f"nats://{server_ip}:{port}"
    print(f"Connecting to {url}...")

    # Connect to the NATS server
    nc = NATS()
    await nc.connect(url)
    print("Connected. Listening for 'ping'...")

    # Define the message handler for 'ping'
    async def handle_ping(msg):
        await nc.publish("pong", msg.data)

    # Subscribe to 'ping' topic: every time a 'ping' is received,
    # the handle_ping function is called which echos back the received msg
    await nc.subscribe("ping", cb=handle_ping)

    # Do this forever, until interrupted
    try:
        while True:
            await asyncio.sleep(1)
    finally:
        await nc.close()
        print("Connection closed.")

def parse_args():
    parser = argparse.ArgumentParser(description="NATS PONG responder")
    parser.add_argument("--server-ip", required=True)
    parser.add_argument("--port", default=4222, type=int)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(run(args.server_ip, args.port))
    except KeyboardInterrupt:
        print("Exiting.")
