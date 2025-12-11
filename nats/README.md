# NATS example

This example shows a simple example that uses the NATS middleware, by creating a publisher and a subscriber. The publisher sends messages on a topic, and the subscriber echoes them back. The Round-Trip Time (RTT) is measured at the publisher side and printed on the console.

## 1. Installing and Running the NATS Server

Download and install the NATS server package on one VM (e.g., VM1):
```bash
curl -fsSL https://binaries.nats.dev/nats-io/nats-server/v2@latest | sh
```

Then start the server on that machine (here, VM1):
```bash
nats-server --addr=<ip> --port=<port>
```
Replace `<ip>` and `<port>` with VM1's IP address and a port number.

## 2. Install the Python client on both VMs

On both VMs, create a virtual environment, activate it, and then install the NATS Python client library:

```bash
pip install nats-py
```

This installs the NATS Python client library, which is required to run the example applications. It is based on `asyncio`, so make sure you have a Python version that supports it.

## 3. Take a look at the Python code 

The example consists of two Python applications: [`ping.py`](ping.py) and [`pong.py`](pong.py). Familiarize yourself with the code in these files to understand how the publisher and subscriber work. In particular, note how the NATS client is initialized, how messages are published and subscribed to, and how message handling is implemented using NATS code.

The `ping` application publishes a message of size `size` on the "ping" topic. The `pong` application subscribes to the "ping" ping topic and echoes back the received messages on the "pong" topic. In turn, `ping` is subscribed to the "pong" topic and, on receiving a message, it computes the RTT.  The NATS server sits in the middle and forwards messages.

## 4. Running the Example

On VM2, run first the pong application:
```bash
python3 pong.py --server-ip <ip> --port <port>
```
Then on VM1, run the ping application:
```bash
python3 ping.py --server-ip <ip> --port <port> --size <size>
```
Replace `<ip>`, `<port>`, and `<size>` with the appropriate values. The `--size` argument specifies the size of the payload in bytes.

