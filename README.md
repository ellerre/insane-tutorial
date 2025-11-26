# INSANE Tutorial

This repository containst the code example for the tutorial of the [INSANE middleware](https://github.com/MMw-Unibo/INSANE). More tutorial information on the [Tutorial Website](https://insane-tutorial.ing.unibo.it). 

## Environment Setup

We will provide .... to the attendant
For those who cannot attend....

### NATS Example Application

This example application shows how to use the NATS middleware to create a simple publisher-subscriber system and evaluate the latency. The application consists of two main components: a publisher that sends messages and a subscriber that receives them. All the material is in the [`nats`](nats) folder.

### INSANE Example Application

This example application demonstrates how to use the INSANE middleware to create a simple publisher-subscriber system and evaluate the latency. The application consists of two main components: a publisher that sends messages and a subscriber that receives them. All the material is in the [`insane`](insane) folder.

The tutorial will guide you through the steps to modify the NATS example application to use the INSANE middleware instead, showing that with minimal and straightforward changes, you can switch from NATS to INSANE, thus maintaining the same application logic but leveraging the features and capabilities of the INSANE middleware, such as the portability across **various kernel-bypass stacks**.

