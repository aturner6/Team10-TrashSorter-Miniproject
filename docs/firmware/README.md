# Project Documentation

## Contents
The MicroPython source for the meeting timer was uploaded to the Seeed XIAO ESP32-S3 via Thonny.

Handles the three device states (picking preset, running, time's up)
Drives the 28BYJ-48 stepper (via the L293D H-bridge) to move the clock hand as time elapses
Reads the two tactile buttons (GPIO5, GPIO6) for preset selection and start/cancel control
Drives the three status LEDs (GPIO7 red, GPIO8 blue, GPIO9 green) with PWM for the pulsing effect

Each function and the pin mapping are explained by inline comments in the code. For complete operating instructions  see the root README.md and the state chart in ../docs/.

---

## Quick Links

- [Firmware]()
- [Electrical]()
- [Enclosure]()
