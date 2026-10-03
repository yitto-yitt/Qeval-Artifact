# EVAL_META: task_id=68, framework=qpanda2, class=1
import pyqpanda as pq
from numpy import pi


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    angle = pi / cycles
    measurements = cycles + 1 if bomb_live else 1
    live_predictions = dud_predictions = detonations = 0

    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        qubit = machine.qAlloc()
        cbits = machine.cAlloc_many(measurements)
        program = pq.QProg()

        for i in range(cycles):
            program << pq.RY(qubit, angle)
            if bomb_live:
                program << pq.Measure(qubit, cbits[i])

        program << pq.Measure(qubit, cbits[-1])
        counts = machine.run_with_configuration(program, cbits, shots)

        if bomb_live:
            for key, value in counts.items():
                if key[0] == "1":
                    detonations += value
                elif "1" in key[1:]:
                    dud_predictions += value
                else:
                    live_predictions += value
        else:
            live_predictions = counts.get("0", 0)
            dud_predictions = counts.get("1", 0)

        return {
            "live_predictions": live_predictions / shots,
            "dud_predictions": dud_predictions / shots,
            "detonations": detonations / shots,
        }
    finally:
        machine.finalize()
