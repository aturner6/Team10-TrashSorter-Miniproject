# Meeting Timer State Flow Diagram

Documents the Ready, Running, Resetting, and Finished states,
including B1 preset selection, B2 start/reset, motor return,
and LED behavior. The diagram retains its original layout,
colors, fonts, and short wording.

- [Mini_Project_State_Diagram.drawio](Mini_Project_State_Diagram.drawio) — editable diagram.
- [Mini_Project_State_Diagram.drawio.pdf](Mini_Project_State_Diagram.drawio.pdf) — viewable PDF.

## Code reference

Matches [firstDraft.py at main commit 19f7ae3](https://github.com/aturner6/Team10-TrashSorter-Miniproject/blob/19f7ae3731c46b1a6b27202ce7752f3b77c4afbd/docs/firmware/firstDraft.py), reviewed September 15, 2026.

- B1 selects the next preset only in Ready, while the hand is not returning.
- B2 starts from Ready. While running, finished, or returning, B2 resets the selected duration and returns the hand if needed.
- Resetting returns to Ready when the hand reaches its starting position. If no return is needed, reset goes directly to Ready.
- Ready and Resetting use steady blue; Running pulses green; Finished pulses red.
- At completion, the hand returns and stops, but the timer stays Finished with red pulsing until B2 resets it.
- There is no pause/resume behavior in this code.

The current code uses **15/20/25/30 seconds**; the minute-based presets are commented out. The diagram labels seconds to match the implementation. The assignment requires minutes, so the team must finalize timing and then update both diagram files if that changes.

Validation: checked state transitions against the referenced source, verified the draw.io structure, and visually checked the regenerated PDF. Physical timing, motor direction, LED wiring, and hardware behavior still require team verification.

Related task: Issue #2 — Flowstate Chart to Assess Operations.
