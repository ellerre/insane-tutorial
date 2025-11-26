import asyncio
import argparse
import time
import nsn
from helper import *
import ctypes

async def run(qos, size):
    # Keep track of the last ping send time
    start_time = None

    # Connect to the NATS server
    nsn.init()
    print("Connected to the INSANE daemon.")

    # Create relevant QoS options
    opts = nsn.nsn_options_t()
    opts.reliability = nsn.NSN_QOS_RELIABILITY_RELIABLE # Unreliable (UDP) or Reliable (TCP)
    opts.datapath = nsn.NSN_QOS_DATAPATH_DEFAULT        # Default or fast
    if qos == "fast":
        opts.datapath = nsn.NSN_QOS_DATAPATH_FAST

    # Create a stream
    stream = nsn.create_stream(opts)

    sink_id = topic_name_to_id("pong")
    sink = nsn.create_sink(stream, sink_id, None)

    src_id = topic_name_to_id("ping")
    src = nsn.create_source(stream, src_id)

    # Keep running until the user kills the app
    try:
        while True:
            
            # Get an INSANE buffer and fill it in-place
            buffer = nsn.get_buffer(size, nsn.NSN_BLOCKING)
            buffer.contents.len = size           
            fill_buffer_with_char(buffer, 'x', size)

            # Send the ping message
            start_time = time.time_ns()
            nsn.emit_data(src, buffer)
            
            # Wait for the pong response and calculate RTT
            buffer = nsn.consume_data(sink, nsn.NSN_BLOCKING)
            if buffer is None:
                print("No response received.")
                continue

            rtt_us = (time.time_ns() - start_time) / 1000
            print(f"RTT {rtt_us:.2f} us")

            # Return the buffer to INSANE
            nsn.release_data(buffer)

            # Wait a second before sending the next ping            
            await asyncio.sleep(1)

    finally:
        await nsn.close()
        print("Connection closed.")

def parse_args():
    parser = argparse.ArgumentParser(description="INSANE PING sender")
    parser.add_argument("--qos", default="default", help="QoS profile (default or fast)")
    parser.add_argument("--size", type=int, default=64, help="Payload size in bytes")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(run(args.qos, args.size))
    except KeyboardInterrupt:
        print("Exiting.")