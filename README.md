# INSANE Tutorial

This repository containst the code example for the tutorial of the [INSANE middleware](https://github.com/MMw-Unibo/INSANE). More tutorial information on the [Tutorial Website](https://insane-tutorial.ing.unibo.it). 

## Environment Setup

For the tutorial participants, we will give participants access to two VMs, already configured and set up for running the INSANE applications. 

For people that cannot attend the tutorial: INSANE can run on either bare-metal machines or VMs, as long as it has enough resources. We recommend at least 8 CPU cores and 8 GB of RAM if all the network plugins are going to be used concurrently. In case of VMs, it is important that the NIC is passed through to the VM using PCI passthrough (e.g., using VFIO). One can pass through the entire NIC or use SR-IOV to create Virtual Functions (VFs) that can be passed through to the VM. Support for virtualized (virtio-based) interfaces is not available at the moment, but it is planned for future releases. Similarly, support for local communication (2+ apps connecting to the same INSANE daemon on the same host) is not supported yet, so you will need two separate hosts (or VMs) for the tutorial.

### NATS Example Application

This example application is the baseline for the tutorial. It shows how to use the NATS middleware to create a simple publisher-subscriber system and evaluate its latency. The application consists of two main components: a sender that periodically sends messages and a receiver that echoes them back. 

Participants are invited to test the application, evaluate its performance, and look at the code. All the material is in the [`nats`](nats) folder.

### INSANE Example Application

This example application is the core of the tutorial. It demonstrates how to use the INSANE middleware to re-create the same application previously considered. The tutorial will guide the participants through the steps to modify the NATS example application to use the INSANE middleware instead, showing that with minimal and straightforward changes, they can switch from NATS to INSANE, thus maintaining the same application logic but leveraging the features and capabilities of the INSANE middleware, such as the portability across **various kernel-bypass stacks**.

This repository already contains the solution; during the tutorials, the transition between NATS and INSANE will be guided through an hands-on activity. All the material is in the [`insane`](insane) folder.



