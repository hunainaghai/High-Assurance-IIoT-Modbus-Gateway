# High-Assurance IIoT Modbus Gateway

## Overview
This project demonstrates a secure Industrial IoT gateway designed to protect Modbus TCP controllers. It focuses on preventing "Semantic Gap" attacks where an adversary exploits inconsistencies between gateway monitoring and PLC logic.

## The Problem: Semantic Inconsistency
Standard industrial gateways often forward traffic without inspecting the payload context. This allows attackers to bypass security states by targeting unmonitored registers.

## The Solution: Deep Packet Inspection (DPI)
This gateway performs real-time hex stream analysis. It implements an immutable security policy that hard-blocks unauthorized write attempts to critical safety registers (e.g., Register 50).



## Project Structure
* `sim_slave.py`: The industrial simulator (Field Zone).
* `gateway.py`: The High-Assurance Gateway (Enforcement Zone).
* `attack_payload.py`: The penetration testing script (Adversary).

## How to Run
1. Start the simulator: `python sim_slave.py`
2. Start the secure gateway: `python gateway.py`
3. Execute the attack test: `python attack_payload.py`

## Results
The gateway successfully identifies the malicious hex signature for Register 50 and drops the packet before it reaches the field device, maintaining a "Zero-Trust" environment.