# EVAL_META: task_id=68, framework=cirq, class=1
import numpy as np
import cirq


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    shots = 1024
    cycles = 25
    e = np.pi / cycles

    q = cirq.LineQubit(0)
    sim = cirq.Simulator()

    if bomb_live:
        c = cirq.Circuit()
        for i in range(cycles):
            c.append(cirq.ry(e).on(q))
            c.append(cirq.measure(q, key=f"m{i}"))
        c.append(cirq.measure(q, key="final"))

        res = sim.run(c, repetitions=shots)

        # In Qiskit big-endian ordering, key[0] corresponds to the highest
        # classical bit = the final measurement.
        final_bits = res.measurements["final"][:, 0]
        det = int(np.sum(final_bits == 1))

        any_int = np.zeros(shots, dtype=bool)
        for i in range(cycles):
            any_int |= (res.measurements[f"m{i}"][:, 0] == 1)

        dud = int(np.sum((final_bits == 0) & any_int))
        live = int(np.sum((final_bits == 0) & (~any_int)))
    else:
        c = cirq.Circuit()
        for _ in range(cycles):
            c.append(cirq.ry(e).on(q))
        c.append(cirq.measure(q, key="m"))

        res = sim.run(c, repetitions=shots)
        bits = res.measurements["m"][:, 0]
        live = int(np.sum(bits == 0))
        dud = int(np.sum(bits == 1))
        det = 0

    return {
        "live_predictions": live / shots,
        "dud_predictions": dud / shots,
        "detonations": det / shots,
    }
