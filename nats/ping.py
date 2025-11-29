import asyncio
import argparse
import time
import nats

async def run(server_ip, port, size):
    url = f"nats://{server_ip}:{port}"
    print(f"Connecting to {url}...")

    payload = b"x" * size
    print(f"Prepared payload of {size} bytes.")

    # Connect to the NATS server
    nc = await nats.connect(url)
    print("Connected.")

    # Subscribe to 'pong' topic: every time a 'pong' is received,
    # the handle_pong function is called which prints the RTT
    sub = await nc.subscribe("pong")

    # Keep running until the user kills the app
    try:
        while True:           
            # Send the ping message
            start_time = time.time_ns()
            await nc.publish("ping", payload)

            # Wait for the reply
            msg = await sub.next_msg()

            # Compute the RTT
            rtt_us = (time.time_ns() - start_time) / 1000
            print(f"RTT {rtt_us:.2f} us")

            # Wait a second before sending the next ping            
            time.sleep(1)
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
