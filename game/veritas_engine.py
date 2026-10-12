import json
import math
import os

class CaseManager:
    """
    Decoupled Case Controller.
    Manages state machines, forensic graphs, and biometric formulas.
    """
    def __init__(self, schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        self.case_id = self.data["case_id"]
        self.evidence = {e["id"]: e for e in self.data["evidence"]}
        self.suspects = self.data["suspects"]
        
        # Runtime State
        self.active_suspect_id = "elena"
        self.suspect_states = {
            s_id: {
                "stress": s_data["base_stress"],
                "trust": 0,
                "broken_claims": set(),
                "cooperative": False
            }
            for s_id, s_data in self.suspects.items()
        }
        self.unlocked_nodes = set()

    def inspect_evidence(self, clue_id):
        """Processes forensic lab analysis on a clue."""
        if clue_id in self.evidence:
            self.evidence[clue_id]["inspected"] = True
            self.unlocked_nodes.add(f"INSPECTED_{clue_id}")
            return True
        return False

    def get_stress(self, suspect_id=None):
        target = suspect_id or self.active_suspect_id
        return round(self.suspect_states[target]["stress"], 1)

    def apply_pressure_tactic(self, tactic_type):
        """
        Calculates stress and trust using biometric delta functions.
        """
        s = self.suspect_states[self.active_suspect_id]
        profile = self.suspects[self.active_suspect_id]

        if tactic_type == "SLAP_TABLE":
            # High intimidation: spikes stress, diminishes trust
            delta = 22.0 * profile["composure_decay"]
            s["stress"] = min(100.0, s["stress"] + delta)
            s["trust"] = max(0, s["trust"] - 1)
            return {"status": "INTIMIDATED", "delta": delta}

        elif tactic_type == "REASSURE":
            # De-escalation: reduces stress, builds rapport
            s["stress"] = max(10.0, s["stress"] - 12.0)
            s["trust"] += 1
            return {"status": "CALMED", "trust": s["trust"]}

        return {"status": "NEUTRAL"}

    def evaluate_contradiction(self, clue_id):
        """
        Evaluates contradiction graph.
        Returns break payload if the evidence matches an inspected vulnerability.
        """
        clue = self.evidence.get(clue_id)
        if not clue:
            return {"success": False, "msg": "Invalid evidence."}

        if not clue["inspected"]:
            return {
                "success": False,
                "msg": "Unverified evidence. Without lab analysis, the suspect dismisses it as circumstantial."
            }

        s_profile = self.suspects[self.active_suspect_id]
        s_state = self.suspect_states[self.active_suspect_id]

        for claim in s_profile["claims"]:
            if claim["contradicted_by"] == clue_id:
                # Contradiction validated
                s_state["broken_claims"].add(claim["id"])
                s_state["stress"] = min(100.0, s_state["stress"] + claim["break_stress_spike"])
                self.unlocked_nodes.add(f"BROKEN_{claim['id']}")
                
                if len(s_state["broken_claims"]) == len(s_profile["claims"]):
                    s_state["cooperative"] = True

                return {
                    "success": True,
                    "admission": claim["admission"],
                    "spike": claim["break_stress_spike"]
                }

        # Clue is inspected but irrelevant to this suspect's active claims
        s_state["stress"] = max(10.0, s_state["stress"] - 5.0)
        return {"success": False, "msg": "Evidence has no direct correlation to current statements."}

    def evaluate_case_outcome(self):
        """
        Determines the final resolution based on cross-examination matrix.
        """
        elena_done = self.suspect_states["elena"]["cooperative"]
        marcus_done = self.suspect_states["marcus"]["cooperative"]
        elena_trust = self.suspect_states["elena"]["trust"]

        if elena_done and marcus_done and elena_trust >= 2:
            return "CLEAN_JUSTICE" # Ideal outcome
        elif self.suspect_states["elena"]["stress"] >= 95.0:
            return "PROCEDURAL_MISCONDUCT" # Over-pressured
        elif not elena_done and not marcus_done:
            return "INSUFFICIENT_EVIDENCE"
        else:
            return "CONTESTED_PLEA"