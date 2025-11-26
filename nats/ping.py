import asyncio
import argparse
import time
from nats.aio.client import Client as NATS

async def run(server_ip, port, size):
    url = f"nats://{server_ip}:{port}"
    print(f"Connecting to {url}...")

    payload = b"x" * size
    print(f"Prepared payload of {size} bytes.")

    # Keep track of the last ping send time
    start_time = None

    # Connect to the NATS server
    nc = NATS()
    await nc.connect(url)
    print("Connected.")

    # Define the message handler for 'pong'
    async def handle_pong(msg):
        nonlocal start_time
        if start_time is None:
            return
        rtt_us = (time.time_ns() - start_time) / 1000
        print(f"RTT {rtt_us:.2f} us")

    # Subscribe to 'pong' topic: every time a 'pong' is received,
    # the handle_pong function is called which prints the RTT
    await nc.subscribe("pong", cb=handle_pong)

    # Keep running until the user kills the app
    try:
        while True:
            
            # Send the ping message
            start_time = time.time_ns()
            await nc.publish("ping", payload)

            # Wait a second before sending the next ping            
            await asyncio.sleep(1)

    finally:
        await nc.close()
        print("Connection closed.")

def parse_args():
    parser = argparse.ArgumentParser(description="NATS PING sender")
    parser.add_argument("--server-ip", required=True)
    parser.add_argument("--port", default=4222, type=int)
    parser.add_argument("--size", required=True, type=int, help="Message size in bytes")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(run(args.server_ip, args.port, args.size))
    except KeyboardInterrupt:
        print("Exiting.")