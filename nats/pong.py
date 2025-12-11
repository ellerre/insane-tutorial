import asyncio
import argparse
import nats

async def run(server_ip, port):
    url = f"nats://{server_ip}:{port}"
    print(f"Connecting to {url}...")

    # Connect to the NATS server
    nc = await nats.connect(url)
    print("Connected. Listening for 'ping'...")

    # Subscribe to 'ping' topic
    sub = await nc.subscribe("ping")

    # Do this forever, until interrupted
    try:
        while True:
            # Wait for incoming messages
            msg = await sub.next_msg(timeout=None)
            # Echo it back on the "pong" topic
            await nc.publish("pong", msg.data)
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
