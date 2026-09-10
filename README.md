# 03-Miniproject-2026-27

This is a repo for a multi-disciplinary mini-project for a
small team of EEs and ME. The mini-project is described in the
course assignment. You should tailor this repo based on your team
composition, roles, and the tasks at hand.

# Project Summary 

This device is a self-contained meeting timer that runs MicroPython on a Seeed XIAO ESP32-S3. The countdown begins after the user uses two tactile buttons to choose a predetermined time (15, 20, 25, or 30 minutes). Three status LEDs (powered with PWM for a pulsating effect) show the device's current condition, and a stepper motor powers an actual clock hand that scrolls down as time passes.

# Description of the device

* Microcontroller: Seeed XIAO ESP32-S3
* Motor: 28BYJ-48 5-wire, 4-phase unipolar stepper, driven through an L293D H-bridge (wave-pulse stepping, one coil energized at a time), moving a popsicle-stick clock hand to show time remaining
* Inputs: two tactile pushbuttons (GPIO5, GPIO6)
* Outputs: three PWM-driven LEDs: red (GPIO7), blue (GPIO8), green (GPIO9), each pulsed at a ~1s duty-cycle rate

# Photo of device 

# How to operate

# Demo video

# References 

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

| Component | Notes |
|-----------|-------|
| Thing 1 | Thing 1 notes  |
| Thing 2 | Thing 2 notes  |

---

## Team Responsibilities 
Any discipline can do any role here -- you make the assigments. 

### Mechanical oriented
- Design the enclosure 
- Fabricate the enclosure (3-D print or laser-cut)
- Document the assembly process 

### Electrical oriented
- Produce the breadboard schematic
- Summarize the bill of materials
- Wire the circuit on the breadboard, verfify that the componets are assembled correctly, validate the voltage levels

### Computer oriented
- Design the software based on the required functionality
- Develop MicroPython code and firmware 
- Flash and test the firmware on the target micro
- Document the APIs for the system

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

1. Establish that each teammember has properly set up Git/GitHub Desktop
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

