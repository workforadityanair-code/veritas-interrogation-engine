# Veritas: State-Graph Driven Forensic Interrogation Engine

An offline, decoupled interrogation engine implemented in Python and Ren'Py. 

Instead of hardcoded script branching, **Veritas** isolates narrative presentation from logic by modeling suspect behavior through a **Deterministic Finite State Machine (FSM)** and an externalized **Forensic Contradiction Graph**.

---

## Architecture Overview

```
 ┌──────────────────────┐
 │   case_schema.json   │ ◄── Externalized Data Layer (Entities, claims, physical clues)
 └──────────┬───────────┘
            ▼
 ┌──────────────────────┐
 │  veritas_engine.py   │ ◄── Domain Logic Layer (FSM, Biometrics, Graph Resolution)
 └──────────┬───────────┘
            ▼
 ┌──────────────────────┐
 │      script.rpy      │ ◄── UI / Presentation Layer (ATL Transforms, HUD, Node Tree)
 └──────────────────────┘
```

---

## Key Technical Features

1. **Decoupled Data Schema (`case_schema.json`)**
   * Case facts, baseline psychological profiles, alibis, and contradiction targets are fully serialized in JSON.
   * New suspects and scenarios can be introduced without modifying engine source code.

2. **Forensic Contradiction Resolution Graph**
   * Physical evidence is stored as state graph nodes.
   * Clues cannot break suspect claims until their state transitions to `inspected = True` via forensic laboratory analysis, enforcing chain-of-custody mechanics.

3. **Biometric Stress & Rapport Dynamics**
   * Suspect states evolve via mathematical decay functions based on tactics used (`SLAP_TABLE`, `REASSURE`).
   * Pushing stress beyond safety thresholds ($Stress \ge 95\%$) triggers procedural shutdown fail-states.

4. **Multi-Suspect Interrogation & Cross-Examination Bus**
   * Dynamic entity swapping between interrogation rooms. Admissions extracted from one suspect unlock contradiction branches against co-conspirators.

5. **Dynamic 3-Tier Mind-Palace Flowchart**
   * Live visual node tree tracking evidence inspection roots, alibi break points, and dual-contradiction convergence.

---

## File Structure

```text
├── game/
│   ├── veritas_engine.py   # Core Python FSM controller and graph logic
│   ├── case_schema.json    # Serialized case, evidence, and suspect schemas
│   ├── script.rpy          # Presentation layer, screens, and ATL transforms
│   ├── images/             # Visual sprites and background composites
│   └── audio/              # Sound assets
├── .gitignore              # Ignores .rpyc, logs, and cache binaries
└── README.md
```

