# 03-Miniproject-2026-27

This is a repo for a multi-disciplinary mini-project for a
small team of EEs and ME. The mini-project is described in the
course assignment. You should tailor this repo based on your team
composition, roles, and the tasks at hand.

Complete the project documentation in your Miniproject repo including:
Project summary (as .md) including 
Description of device 
Photo(s) of device
Description of how to use your device
Record a link to your device in operation (< 10s) and link to file stored in your team google team folder under /video
References to any source materials adopted in the project
Project support documents
Flowcharts and or/state charts of system 
Schematic of device (no fritzing please) 
Mechanical design and CAD drawings/STLs of enclosure (if MEs on team)
Code folder including embedded code comments
Simple readme.md in each subfolder


# Project Summary 

This device is a self-contained meeting timer that runs MicroPython on a Seeed XIAO ESP32-S3. The countdown begins after the user uses two tactile buttons to choose a predetermined time (15, 20, 25, or 30 minutes). Three status LEDs (powered with PWM for a pulsating effect) show the device's current condition, and a stepper motor powers an actual clock hand that scrolls down as time passes.

# Description of the device

* Microcontroller: Seeed XIAO ESP32-S3
* Motor: 28BYJ-48 5-wire, 4-phase unipolar stepper, driven through an L293D H-bridge (wave-pulse stepping, one coil energized at a time), moving a popsicle-stick clock hand to show time remaining
* Inputs: two tactile pushbuttons (GPIO5, GPIO6)
* Outputs: three PWM-driven LEDs: red (GPIO7), blue (GPIO8), green (GPIO9), each pulsed at a ~1s duty-cycle rate

# Photo of device 

# How to operate
Connect and turn on the power. The blue LED will then illuminate. Select the Modes 15, 20, 25, and 30 (min) which are cycled by the left button (Button 1). The timer can be started or stopped by pressing the right button (Button 2). Timer moves clockwise (CW) until it hits the set time, then resets back to start — until Button 2 is pressed again to change mode.\
LED states: Red indicates the time is up, Green indicates the timer is active, and Blue indicates cycling (mode choose).
# Demo video
  [Demo Google Drive Video](https://drive.google.com/file/d/13cO3BlyUWwyqgb_B9XeeHkqI3Kim0GOf/view?usp=drive_link)
# References 
Reference we used for PWM LED [LinuxHint](https://linuxhint.com/pwm-esp32-micropython-thonny-ide/)

# Flowchart of the system
The flow chart of the system is [State Diagram](docs/state-flow/Mini_Project_State_Diagram.drawio.pdf) — viewable PDF.
# Schematic of the device
The schematic chart of the system is [Schematic Chart](docs/hardware/electrical/MINIPROJECTDIAGRAM.pdf) — viewable PDF.
# Mechanical design and CAS drawings/STLs of enclosure
All the mechanical designs and STL files are in [Mechanical](docs/hardware/mechanical)

# Code folder

The code folder is in [Firmware](docs/firmware)

---

## Team

| Role | Named Members |
|------|---------|
| Mechanical Engineering | John |
| Electrical Engineering | Adina, Rebecca, Richard, Carlos |

---

## Repository Structure

```
.
├── firmware/          # Micro source code
├── hardware/
│   ├── electrical/    # Schematics, wiring diagrams, and BOM
│   └── mechanical/    # Enclosure CAD files and fabrication notes
└── docs/              # Project documentation 
```

---

## Hardware

| Component | Description|
|-------------|--------- | 
| Seeed XIAO ESP32-S3, pre-soldered |Microcontroller for the clock|
| Multi-color LED |Visual indicator of status|
| Breadboard |Used for connections of all other components. |
| Tactile breadboard switch |One button cycles time duration, another starts and stops|	
 | 220-ohm resistor |adds resistance to circuit|
 | Battery holder, 3x AAA cells |powers the timer|
 | Stepper motor |moves the handles in steps for timer|
 | Motor driver (L293D) |6 step control|
 | Jumper wire kit |used to connect all the components on breadboard|

---

## Team Responsibilities 
Any discipline can do any role here -- you make the assigments. 

### Mechanical oriented - John Colcha
- Design the enclosure 
- Fabricate the enclosure (3-D print or laser-cut)
- Document the assembly process 

### Electrical oriented - Carlos Rivas, Adina Turner, Richard Huang
- Produce the breadboard schematic - Adina Turner
- Summarize the bill of materials - Carlos Rivas
- Wire the circuit on the breadboard, verify that the components are assembled correctly, validate the voltage levels - Adina Turner
- Develop flowchart for the time device - Richard Huang

### Computer oriented - Rebecca Brautigam, Carlos Rivas
- Design the software based on the required functionality - Rebecca Brautigam
- Develop MicroPython code and firmware - Rebecca Brautigam
- Flash and test the firmware on the target micro - Rebecca Brautigam
- Document the project on the repo and record 10 second video - Carlos Rivas

## Deliverables

- [ ] Functional MicroPython firmware
- [ ] Completed breadboard assembly per schematic
- [ ] Fabricated and assembled enclosure (if MEs on team)
- [ ] Documentation in this repository
- [ ] Video recording demonstrating required function (stored in google drive)

## Contribution Workflow

We want each team member to contribute work products and to host these
including documentation in the repo with version control (software,
firmware, schematics, BOMs, CAD models, etc.) All can be managed in
the repo with version control.

1. Establish that each team member has properly set up Git/GitHub Desktop
2. Decompose the project into units to assign to each named team member 
3. From the team repo, create a branch from `main` named `<role>/<feature>` (e.g., `me/case`) to capture work artifacts 
4. Fetch the branch to the local laptop
5. Each team member does their work and produces work artifacts and commits these changes to the branch
6. Commit changes with descriptive messages
7. Open a pull request and request review from at least one other team member
8. Merge to main after approval

When performed properly, this workflow leads to an organized set of
work products that are developed concurrently and collaboratively with
version control. This includes the products themselves (e.g.,
firmware, CAD, schematics, etc.) and the associated documentation

Don't know how to do this? Ask your ECE teammates, GSTs, instructors, or AI. 

---

