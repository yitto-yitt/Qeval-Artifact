# EVAL_META: task_id=68, framework=qpanda, class=1
import pyqpanda3.core as pq
from math import pi

def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    measurements = cycles + 1 if bomb_live else 1
    measure = getattr(pq, "measure", None) or getattr(pq, "Measure")

    program = pq.QProg()
    for i in range(cycles):
        program << pq.RY(0, pi / cycles)
        if bomb_live:
            program << measure(0, i)
    program << measure(0, measurements - 1)

    simulator = pq.CPUQVM()
    result = simulator.run(program, shots)
    if not hasattr(result, "get_counts"):
        result = simulator.result()
    counts = result.get_counts()

    live_predictions = 0
    dud_predictions = 0
    detonations = 0

    for key, count in counts.items():
        if isinstance(key, int):
            bits = format(key, f"0{measurements}b")
        else:
            bits = str(key).replace(" ", "").zfill(measurements)

        if bomb_live:
            if bits[0] == "1":
                detonations += count
            elif "1" in bits[1:]:
                dud_predictions += count
            else:
                live_predictions += count
        elif bits[-1] == "1":
            dud_predictions += count
        else:
            live_predictions += count

    return {
        "live_predictions": live_predictions / shots,
        "dud_predictions": dud_predictions / shots,
        "detonations": detonations / shots,
    }
