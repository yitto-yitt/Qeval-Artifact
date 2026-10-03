# EVAL_META: task_id=68, framework=qpanda2, class=1
from pyqpanda import *
from math import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = pi / cycles
    measurements = cycles + 1 if bomb_live else 1

    machine = CPUQVM()
    machine.init_qvm()
    try:
        qubits = machine.qAlloc_many(2 if bomb_live else 1)
        q = qubits[0]
        cbits = machine.cAlloc_many(measurements)

        if bomb_live:
            cal_q = qubits[1]
            bit_position = {}
            for target in range(measurements):
                cal_prog = QProg()
                for i in range(measurements):
                    if i == target:
                        cal_prog.insert(X(cal_q))
                        cal_prog.insert(Measure(cal_q, cbits[i]))
                        cal_prog.insert(X(cal_q))
                    else:
                        cal_prog.insert(Measure(cal_q, cbits[i]))
                cal_counts = dict(machine.run_with_configuration(cal_prog, cbits, 1))
                cal_key = next(iter(cal_counts.keys()))
                positions = [idx for idx, ch in enumerate(cal_key) if ch == "1"]
                bit_position[target] = positions[0] if positions else (measurements - 1 - target)

        prog = QProg()
        for i in range(cycles):
            prog.insert(RY(q, e))
            if bomb_live:
                prog.insert(Measure(q, cbits[i]))
        prog.insert(Measure(q, cbits[measurements - 1]))

        counts = dict(machine.run_with_configuration(prog, cbits, shots))

        live_predictions = 0
        dud_predictions = 0
        detonations = 0

        if bomb_live:
            final_pos = bit_position[measurements - 1]
            intermediate_positions = [bit_position[i] for i in range(cycles)]
            for key, value in counts.items():
                if key[final_pos] == "1":
                    detonations += value
                elif any(key[pos] == "1" for pos in intermediate_positions):
                    dud_predictions += value
                else:
                    live_predictions += value
        else:
            live_predictions = counts.get("0", 0)
            dud_predictions = counts.get("1", 0)
            detonations = 0

        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }
    finally:
        machine.finalize()
