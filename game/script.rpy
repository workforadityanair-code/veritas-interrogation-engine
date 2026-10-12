# ==========================================================
# VERITAS: STATE-GRAPH DRIVEN FORENSIC INTERROGATION ENGINE
# ==========================================================

init python:
    import os
    import renpy.exports as renpy
    from veritas_engine import CaseManager

    schema_file = os.path.join(renpy.config.gamedir, "case_schema.json")
    case = CaseManager(schema_file)

# 1. CHARACTER DEFINITIONS
define p = Character("DETECTIVE", color="#38bdf8")
define elena = Character("Elena Rostova", color="#f43f5e")
define marcus = Character("Marcus Vance", color="#f59e0b")
define log = Character("TRANSCRIPT", color="#94a3b8")

# ==========================================================
# 2. VISUAL ASSETS & ROOM BACKGROUND
# ==========================================================

# Clean Interrogation Room Background
image bg_interrogation = Transform("images/bg_room.jpg", xsize=1920, ysize=1080)

# Suspect 1: Elena Rostova
image elena neutral:
    "images/elena_normal.png"
    yalign 1.0 xalign 0.5 zoom 0.85

image elena shaken:
    "images/elena_shocked.png"
    yalign 1.0 xalign 0.5 zoom 0.85

# Suspect 2: Marcus Vance
image marcus neutral:
    "images/marcus_normal.jpg"
    yalign 1.0 xalign 0.5 zoom 0.85

image marcus shaken:
    "images/marcus_normal.jpg"
    yalign 1.0 xalign 0.5 zoom 0.85
    matrixcolor TintMatrix("#f87171")

# ==========================================================
# 3. PROCEDURAL ATL CHARACTER ANIMATIONS
# ==========================================================
transform breathing_idle:
    subpixel True
    yoffset 0
    easein 2.2 yoffset -8 zoom 0.855
    easeout 2.2 yoffset 0 zoom 0.850
    repeat

transform flinch_backward:
    subpixel True
    easein 0.08 yoffset 24 zoom 0.83
    easeout 0.25 yoffset 0 zoom 0.85

transform stress_tremble:
    subpixel True
    choice:
        linear 0.05 xoffset -3 yoffset 2
    choice:
        linear 0.05 xoffset 3 yoffset -2
    choice:
        linear 0.05 xoffset 0 yoffset 0
    repeat

# ==========================================================
# 4. POLICE INTERFACE & MODAL SCREENS
# ==========================================================

screen police_hud():
    zorder 10
    frame:
        xalign 0.98 yalign 0.03
        background "#0f172ae6"
        padding (16, 12)
        vbox:
            spacing 4
            $ curr_name = case.suspects[case.active_suspect_id]["name"]
            $ curr_stress = case.get_stress()
            text "SUSPECT: [curr_name]" size 13 color "#f43f5e" bold True
            text "STRESS LEVEL: [curr_stress]%" size 12 color "#38bdf8"
            bar value curr_stress range 100 xsize 240 ysize 10

    hbox:
        xalign 0.02 yalign 0.03
        spacing 10
        textbutton "EVIDENCE DOSSIER" action Show("case_evidence_dossier") style "police_hud_btn"
        textbutton "STATE GRAPH" action Show("case_flowchart_modal") style "police_hud_btn"
        if case.active_suspect_id == "elena":
            textbutton "TRANSFER TO MARCUS (ROOM 2)" action Jump("goto_marcus") style "police_switch_btn"
        else:
            textbutton "TRANSFER TO ELENA (ROOM 1)" action Jump("goto_elena") style "police_switch_btn"

    add Solid("#0b0f19") xsize 1920 ysize 85 yalign 1.0

screen case_evidence_dossier():
    modal True
    zorder 20
    add Solid("#000000cc")
    frame:
        xalign 0.5 yalign 0.5
        xsize 940 ysize 620
        background "#0b1120f5"
        padding (24, 24)
        vbox:
            spacing 14
            text "CASE FILE // FORENSIC EVIDENCE GRAPH" size 18 color "#38bdf8" bold True
            null height 6
            hbox:
                spacing 20
                for e_id in case.evidence:
                    $ item = case.evidence[e_id]
                    $ item_name = item["name"]
                    $ item_raw = item["raw_description"]
                    $ item_analyzed = item["analyzed_data"]
                    $ is_done = item["inspected"]
                    frame:
                        xsize 420 ysize 400
                        background "#1e293b"
                        vbox:
                            spacing 10
                            text "[item_name]" size 14 color "#f59e0b" bold True
                            text "[item_raw]" size 12 color "#cbd5e1"
                            null height 8
                            if is_done:
                                text "[[LAB VERIFIED]]\n[item_analyzed]" size 12 color "#4ade80"
                            else:
                                text "Status: Uninspected" size 12 color "#64748b"
                                textbutton "RUN LAB FORENSICS" action Function(case.inspect_evidence, e_id) style "inspect_btn"

            null height 10
            textbutton "CLOSE DOSSIER" action Hide("case_evidence_dossier") xalign 0.5 style "police_hud_btn"

screen case_flowchart_modal():
    modal True
    zorder 20
    add Solid("#000000dd")
    
    frame:
        xalign 0.5 yalign 0.5
        xsize 1160 ysize 680
        background "#060a14f8"
        padding (28, 24)
        
        vbox:
            spacing 18
            
            # Header
            hbox:
                spacing 15
                text "CASE ARCHITECTURE // FORENSIC STATE GRAPH" size 19 color "#38bdf8" bold True
                text "[[DETECTION TREE VIEW]]" size 12 color "#64748b" yalign 0.5
            
            text "State machine dependency graph. Unlocked nodes glow green with verified forensic links:" size 12 color "#94a3b8"
            
            null height 10

            # 3-Tier Horizontal Tree
            hbox:
                spacing 16
                xalign 0.5

                # ---------------------------------------------
                # TIER 1: PHYSICAL EVIDENCE ROOTS
                # ---------------------------------------------
                vbox:
                    spacing 16
                    xsize 280
                    text "STAGE 1: FORENSIC INPUT" size 12 color "#38bdf8" bold True

                    # Node: CCTV
                    $ cctv_active = "INSPECTED_E_CCTV" in case.unlocked_nodes
                    frame:
                        xsize 280 ysize 105
                        background ("#0e2a22" if cctv_active else "#0f172a")
                        vbox:
                            spacing 4
                            text "TRAFFIC CAM #4TH" size 13 color ("#4ade80" if cctv_active else "#64748b") bold True
                            text "Hash: E_CCTV" size 10 color "#475569"
                            text ("STATUS: ENHANCED & MATCHED" if cctv_active else "STATUS: RAW FOOTAGE [[LOCKED]]") size 10 color ("#86efac" if cctv_active else "#64748b")

                    # Node: Pistol
                    $ gun_active = "INSPECTED_E_FIREARM" in case.unlocked_nodes
                    frame:
                        xsize 280 ysize 105
                        background ("#0e2a22" if gun_active else "#0f172a")
                        vbox:
                            spacing 4
                            text "9MM SERVICE PISTOL" size 13 color ("#4ade80" if gun_active else "#64748b") bold True
                            text "Hash: E_FIREARM" size 10 color "#475569"
                            text ("STATUS: PALM PRINT LIFTED" if gun_active else "STATUS: UNPROCESSED [[LOCKED]]") size 10 color ("#86efac" if gun_active else "#64748b")

                # Tree Connectors Column 1 -> 2
                vbox:
                    spacing 70
                    yalign 0.55
                    text ("────►" if cctv_active else "····►") size 18 color ("#4ade80" if cctv_active else "#334155") bold True
                    text ("────►" if gun_active else "····►") size 18 color ("#4ade80" if gun_active else "#334155") bold True

                # ---------------------------------------------
                # TIER 2: CONTRADICTION NODES
                # ---------------------------------------------
                vbox:
                    spacing 16
                    xsize 310
                    text "STAGE 2: ALIBI CONTRADICTIONS" size 12 color "#f59e0b" bold True

                    # Node: Elena Broken
                    $ elena_broken = "BROKEN_CLM_ELENA_ALIBI" in case.unlocked_nodes
                    frame:
                        xsize 310 ysize 105
                        background ("#1a2a16" if elena_broken else "#0f172a")
                        vbox:
                            spacing 4
                            text "ELENA: BUS ALIBI SHATTERED" size 13 color ("#4ade80" if elena_broken else "#64748b") bold True
                            text "Target: Room 01 (Lookout Role)" size 10 color "#475569"
                            text ("ADMISSION: WATCHED DELIVERY GATE" if elena_broken else "PENDING CONFRONTATION") size 10 color ("#a7f3d0" if elena_broken else "#64748b")

                    # Node: Marcus Broken
                    $ marcus_broken = "BROKEN_CLM_MARCUS_ALIBI" in case.unlocked_nodes
                    frame:
                        xsize 310 ysize 105
                        background ("#1a2a16" if marcus_broken else "#0f172a")
                        vbox:
                            spacing 4
                            text "MARCUS: PUB ALIBI SHATTERED" size 13 color ("#4ade80" if marcus_broken else "#64748b") bold True
                            text "Target: Room 02 (Gun Discharge)" size 10 color "#475569"
                            text ("ADMISSION: FATAL STRUGGLE WITH GUARD" if marcus_broken else "PENDING CONFRONTATION") size 10 color ("#a7f3d0" if marcus_broken else "#64748b")

                # Tree Connectors Column 2 -> 3
                vbox:
                    yalign 0.55
                    $ both_cracked = elena_broken and marcus_broken
                    text ("─────┐\n     ├───►\n─────┘" if both_cracked else "·····┐\n     ├───►\n·····┘") size 16 color ("#4ade80" if both_cracked else "#334155") bold True

                # ---------------------------------------------
                # TIER 3: CASE CONVERGENCE (FINAL LEVERAGE)
                # ---------------------------------------------
                vbox:
                    spacing 16
                    xsize 280
                    yalign 0.55
                    text "STAGE 3: VERDICT" size 12 color "#a855f7" bold True

                    frame:
                        xsize 280 ysize 140
                        background ("#241538" if both_cracked else "#0f172a")
                        vbox:
                            spacing 6
                            text "IDEAL CASE RESOLUTION" size 13 color ("#c084fc" if both_cracked else "#64748b") bold True
                            text ("CONVERGENCE ACHIEVED\nFull corroborated confessions ready for prosecution." if both_cracked else "REQUIRES DUAL CONTRADICTIONS\nCross-examination incomplete.") size 10 color ("#e9d5ff" if both_cracked else "#64748b")

            null height 14
            textbutton "RETURN TO INTERROGATION" action Hide("case_flowchart_modal") xalign 0.5 style "police_hud_btn"

style police_hud_btn:
    background "#1e293b" hover_background "#38bdf8" padding (10, 6)
style police_hud_btn_text:
    color "#f1f5f9" hover_color "#020617" size 11 bold True
style police_switch_btn:
    background "#1e293b" hover_background "#f59e0b" padding (10, 6)
style police_switch_btn_text:
    color "#f59e0b" hover_color "#020617" size 11 bold True
style inspect_btn:
    background "#0f172a" hover_background "#4ade80" padding (8, 6)
style inspect_btn_text:
    color "#cbd5e1" hover_color "#020617" size 11 bold True

# ==========================================================
# 5. SCENE EXECUTION: ROOM 1 (ELENA ROSTOVA)
# ==========================================================

label start:
    show screen police_hud
    scene bg_interrogation with fade

    log "MAJOR CRIMES DIVISION // RECORDING INITIATED."
    log "Case ID: [case.case_id]"

    show elena neutral at center, breathing_idle with dissolve
    elena "I already told your officers—I was just catching the bus on 4th Street. I don't know anything about a homicide."

    jump elena_loop

label elena_loop:
    $ case.active_suspect_id = "elena"
    if case.get_stress("elena") >= 95.0:
        jump resolve_case

    menu:
        "Demand timeline of movements":
            p "Account for your timeline between 22:00 and 22:30."
            $ claim_stmt = case.suspects["elena"]["claims"][0]["statement"]
            elena "[claim_stmt]"
            jump elena_loop

        "Reassure suspect (Build Rapport)":
            $ res = case.apply_pressure_tactic("REASSURE")
            p "Elena, I reviewed your file. You don't have a record. Cooperate with us and we will talk to the prosecutor."
            show elena neutral at center, breathing_idle
            elena "I've worked honest shifts my whole life, Detective. I'm not a killer."
            jump elena_loop

        "SLAM DESK (Aggressive Intimidation)":
            with hpunch
            show elena neutral at center, flinch_backward
            $ res = case.apply_pressure_tactic("SLAP_TABLE")
            p "{b}A GUARD DIED TONIGHT! STOP LYING TO US!{/b}"
            if case.get_stress("elena") >= 50.0:
                show elena shaken at center, stress_tremble with dissolve
                elena "*flinches* Stop screaming at me! You can't beat a confession out of me!"
            else:
                elena "*flinches* Keep your hands off the table! I know my rights!"
            jump elena_loop

        "Confront with Evidence":
            jump elena_confront_evidence

        "Conclude Interrogation & File Charges":
            jump resolve_case

label elena_confront_evidence:
    menu:
        "Confront with Alley Traffic Camera":
            $ outcome = case.evaluate_contradiction("E_CCTV")
            if outcome["success"]:
                with vpunch
                show elena shaken at center, stress_tremble
                $ adm = outcome["admission"]
                p "We enhanced the corner footage. That's your navy coat and watch under the gate for 22 continuous minutes."
                elena "[adm]"
            else:
                $ msg = outcome["msg"]
                elena "[msg]"
            jump elena_loop

        "Confront with 9mm Service Pistol":
            $ outcome = case.evaluate_contradiction("E_FIREARM")
            $ msg = outcome["msg"]
            elena "[msg]"
            jump elena_loop

        "Back":
            jump elena_loop

# ==========================================================
# 6. SCENE EXECUTION: ROOM 2 (MARCUS VANCE)
# ==========================================================

label goto_marcus:
    $ case.active_suspect_id = "marcus"
    scene bg_interrogation with fade
    log "TRANSFERRING TO INTERROGATION ROOM 2 // SUSPECT: MARCUS VANCE"
    show marcus neutral at center, breathing_idle with dissolve
    marcus "Save your breath, Detective. I was three miles away at O'Malley's Pub paying cash."
    jump marcus_loop

label goto_elena:
    $ case.active_suspect_id = "elena"
    scene bg_interrogation with fade
    log "TRANSFERRING TO INTERROGATION ROOM 1 // SUSPECT: ELENA ROSTOVA"
    if case.get_stress("elena") >= 50.0:
        show elena shaken at center, stress_tremble with dissolve
    else:
        show elena neutral at center, breathing_idle with dissolve
    jump elena_loop

label marcus_loop:
    $ case.active_suspect_id = "marcus"
    menu:
        "Interrogate alibi":
            $ claim_stmt = case.suspects["marcus"]["claims"][0]["statement"]
            p "Who saw you at O'Malley's Pub?"
            marcus "[claim_stmt]"
            jump marcus_loop

        "Confront with Discarded 9mm Pistol":
            $ outcome = case.evaluate_contradiction("E_FIREARM")
            if outcome["success"]:
                with vpunch
                show marcus shaken at center, stress_tremble
                $ adm = outcome["admission"]
                p "Our crime lab matched ballistics to the fatal shot and pulled your palm print directly from the grip!"
                marcus "[adm]"
            else:
                $ msg = outcome["msg"]
                marcus "[msg]"
            jump marcus_loop

        "Confront with Alley Traffic Camera":
            $ outcome = case.evaluate_contradiction("E_CCTV")
            $ msg = outcome["msg"]
            marcus "[msg]"
            jump marcus_loop

        "Return to Room 1 (Elena)":
            jump goto_elena

# ==========================================================
# 7. CASE RESOLUTION MATRIX
# ==========================================================

label resolve_case:
    $ final_outcome = case.evaluate_case_outcome()

    if final_outcome == "CLEAN_JUSTICE":
        scene black with fade
        centered "{b}{color=#4ade80}CASE RESOLUTION: FULL CONFESSION SECURED (IDEAL){/color}{/b}\nElena's coercion was verified and Marcus admitted to firing the shot.\nAll forensic contradictions resolved through data state graph."
    elif final_outcome == "PROCEDURAL_MISCONDUCT":
        with hpunch
        scene black with fade
        centered "{b}{color=#f43f5e}CASE RESOLUTION: PROCEDURAL MISCONDUCT (FAILED){/color}{/b}\nExcessive uncalculated pressure induced acute distress; suspect invoked legal silence."
    else:
        scene black with fade
        centered "{b}{color=#64748b}CASE RESOLUTION: INSUFFICIENT EVIDENCE (UNSOLVED){/color}{/b}\nState machine could not reconcile contradictions before holding limit expired."

    return