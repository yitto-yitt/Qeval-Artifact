# EVAL_META: task_id=68, framework=qpanda, class=1
from math import pi
from pyqpanda3.core import CPUQVM, QProg, RY, X, measure


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    measurements = cycles + 1 if bomb_live else 1
    program = QProg()

    # Boundary markers make classical-bit ordering unambiguous.
    program << measure(1, 0)
    for i in range(cycles):
        program << RY(0, pi / cycles)
        if bomb_live:
            program << measure(0, i + 1)
    program << measure(0, measurements)
    program << X(1)
    program << measure(1, measurements + 1)

    simulator = CPUQVM()
    result = simulator.run(program, shots)
    if not hasattr(result, "get_counts"):
        result = simulator.result()
    counts = result.get_counts()

    totals = {
        "live_predictions": 0,
        "dud_predictions": 0,
        "detonations": 0,
    }
    width = measurements + 2
    for key, count in counts.items():
        if isinstance(key, int):
            bits = format(key, f"0{width}b")
        else:
            bits = str(key).replace(" ", "")
            if bits.startswith("0b"):
                bits = bits[2:]
            bits = bits.zfill(width)

        if bits[0] == "0":
            bits = bits[::-1]
        outcomes = bits[1:-1]

        if bomb_live:
            if outcomes[0] == "1":
                totals["detonations"] += count
            elif "1" in outcomes[1:]:
                totals["dud_predictions"] += count
            else:
                totals["live_predictions"] += count
        elif outcomes[0] == "1":
            totals["dud_predictions"] += count
        else:
            totals["live_predictions"] += count

    return {name: count / shots for name, count in totals.items()}
