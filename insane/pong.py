import asyncio
import argparse
import nsn

from helper import topic_name_to_id

async def run(qos):

    # Connect to the INSANE daemon
    nsn.init()
    print("Connected to the daemon. Listening for 'ping'...")

    # Create relevant QoS options
    opts = nsn.nsn_options_t()
    opts.reliability = nsn.NSN_QOS_RELIABILITY_RELIABLE # Unreliable (UDP) or Reliable (TCP)
    opts.datapath = nsn.NSN_QOS_DATAPATH_DEFAULT        # Default or fast
    if qos == "fast":
        opts.datapath = nsn.NSN_QOS_DATAPATH_FAST

    # Create a stream
    stream = nsn.create_stream(opts)

    # Create a source to reply messages
    # by hashing the topic name 'pong'
    src_id = topic_name_to_id("pong")
    src = nsn.create_source(stream, src_id)

    # Create a sink to receive messages
    # by hashing the topic name 'ping'
    sink_id = topic_name_to_id("ping")
    snk = nsn.create_sink(stream, sink_id, None)

    try:
        while True:
            buffer = nsn.consume_data(snk, nsn.NSN_BLOCKING)
            # Echo it back
            if buffer is not None:
                nsn.emit_data(src, buffer)
    finally:
        nsn.close()
        print("Connection closed.")

def parse_args():
    parser = argparse.ArgumentParser(description="ISNANE PONG sender")
    parser.add_argument("--qos", default="default", help="QoS profile (default or fast)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(run(args.qos))
    except KeyboardInterrupt:
        print("Exiting.")
