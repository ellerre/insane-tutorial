# INSANE example

This example shows a simple example that uses the INSANE middleware, by creating a publisher and a subscriber. The publisher sends messages on a topic, and the subscriber echoes them back. The Round-Trip Time (RTT) is measured at the publisher side and printed on the console.

## 1. Installing and Running the INSANE daemon

TODO: ON BOTH MACHINES download the binary of the INSANE daemon

Once you have the binaries, you must set up the configuration file. A sample configuration file named `nsnd.cfg` is provided in this repository: please update it according to your network setup. 
In particular, while the socket-based plugins (UDP and TCP) only need the local ip address they will bind to, the DPDK plugins also need the **PCI address** of the network interface card (NIC) to use. Please refer to the [DPDK documentation](https://doc.dpdk.org/guides/tools/devbind.html) on how to find the PCI address of your NIC and how to set it up for DPDK usage. Note that INSANE has been tested with NVIDIA (mlx5) and a few Intel (i40e) NICs. Other NICs might work, but they are not officially supported.

After preparing the configuration file, you can start the INSANE daemon **on both the VMS** with the following command:

```bash
sudo ./nsnd [--config nsnd.cfg]
```

The `--config` argument specifies the configuration file to use. If not provided, the daemon will look for a file named `nsnd.cfg` in the current directory.

Please note that, in addition to the binary file `nsnd`, a directory named `datapaths` has been created. It contains a number of dynamic libraries that implement the INSANE network operations for different stacks (e.g., sockets, DPDK, RDMA, etc.). These are loaded by the INSANE daemon at runtime based on the user-defined QoS profiles (see later steps for more details).

## 2. Configure the client library

Together with the INSANE daemon, the downloaded package already contains:
- The Python bindings for the INSANE middleware (the `nsn` module)
- The INSANE user library (the `libnsn.so` shared library)

Importantly, before executing the applications, please make sure that the application's configuration file named `nsn-app.cfg` is present in the same directory where you run the applications, on both VMs. A sample configuration file is provided in this repository, which should suffice for this tutorial.

## 3. Take a look at the code 

The example consists of two Python applications: [`ping.py`](ping.py) and [`pong.py`](pong.py). These are the same applications used in the [NATS example](../nats), but modified to use the INSANE middleware. Note that the code is very similar, with minimal differences. Note also that such differences might be hidden behind an abstration layer that exposes to the application the same API as NATS, but the code here does not use such abstraction layer for clarity.

Also, please remember that the INSANE middleware is fully decentralized, so instead of running a central server, both applications connect to the INSANE daemon running locally on each VM.

## 4. Running the Example

Before running the example, please make sure that the INSANE daemon is running on both VMs, and that in the directory where you run the applications there is a configuration file named `nsn-app.cfg` with the appropriate configuration.

On VM2, run first the pong application:
```bash
sudo python3 pong.py [--qos <qos>]
```
Then on VM1, run the ping application:
```bash
sudo python3 ping.py [--qos <qos>] [--size <size>]
```
The `--size` argument specifies the size of the payload in bytes (default 64 bytes).

The `--qos` argument specifies the QoS profile to use. It can be either `default` (default) or `fast`. The `fast` profile uses network acceleration (DPDK) to reduce latency.

Note that the use of `sudo` is required to run these applications, as the INSANE daemon needs access to low-level networking features, and the applications exchange data with it using hugepages. This latter constraint might be removed by switching to regular-sized pages, but that would hurt performance.

## 5. Observing the Output
Note the performance difference between the two QoS profiles. The `fast` profile should yield significantly lower round-trip times (RTT) compared to the `default` profile. Without any code changes or specific system expertise, INSANE allows you to benefit from advanced networking features that enhance performance. Furthermore, porting existing applications to INSANE is straightforward, as demonstrated by the minimal changes required to adapt the NATS ping-pong example to use INSANE.

Importantly, although it is not part of this tutorial, INSANE offers an interception library that can transparently redirect existing socket-based applications to use INSANE without any code modifications. This feature further simplifies the adoption of INSANE in existing systems. You can find such interception library and related documentation on the [INSANE GitHub repository](https://github.com/MMw-Unibo/INSANE).