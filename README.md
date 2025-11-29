# INSANE Tutorial

This repository containst the code example for the tutorial of the [INSANE middleware](https://github.com/MMw-Unibo/INSANE). More tutorial information on the [Tutorial Website](https://insane-tutorial.ing.unibo.it). 

## Environment Setup

For the tutorial participants, we will provide each participants access to two VMs, so to enable them to do a true hands-on activity. The VMs will be equipped with... TODO 

For those who cannot attend....

### NATS Example Application

This example application is the baseline for the tutorial. It shows how to use the NATS middleware to create a simple publisher-subscriber system and evaluate its latency. The application consists of two main components: a sender that periodically sends messages and a receiver that echoes them back. 

Participants are invited to test the application, evaluate its performance, and look at the code. All the material is in the [`nats`](nats) folder.

### INSANE Example Application

This example application is the core of the tutorial. It demonstrates how to use the INSANE middleware to re-create the same application previously considered. The tutorial will guide the participants through the steps to modify the NATS example application to use the INSANE middleware instead, showing that with minimal and straightforward changes, they can switch from NATS to INSANE, thus maintaining the same application logic but leveraging the features and capabilities of the INSANE middleware, such as the portability across **various kernel-bypass stacks**.

This repository already contains the solution; during the tutorials, the transition between NATS and INSANE will be guided through an hands-on activity. All the material is in the [`insane`](insane) folder.



