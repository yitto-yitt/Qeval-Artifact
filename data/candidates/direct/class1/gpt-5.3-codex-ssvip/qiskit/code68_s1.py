# EVAL_META: task_id=68, framework=qiskit, class=1
import math
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def zeno_elitzur_vaidman_bomb_tester(bomb_live):
    cycles = 25
    theta = math.pi / (2 * cycles)

    qr_qubits = 2
    c_qubits = 2
    qc = QuantumCircuit(qr_qubits, c_qubits)

    if bomb_live:
        qc.reset(1)

    for _ in range(cycles):
        qc.ry(2 * theta, 0)
        if bomb_live:
            qc.cx(0, 1)
            qc.measure(1, 1)
            qc.reset(1)

    qc.measure(0, 0)

    simulator = AerSimulator()
    shots = 200000
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()

    detonations = 0
    live_predictions = 0
    dud_predictions = 0

    for bitstring, count in counts.items():
        bits = bitstring.replace(" ", "")
        if len(bits) < 2:
            bits = bits.rjust(2, "0")
        c1 = bits[-2]
        c0 = bits[-1]

        if bomb_live:
            if c1 == "1":
                detonations += count
            else:
                if c0 == "0":
                    live_predictions += count
                else:
                    dud_predictions += count
        else:
            if c0 == "1":
                dud_predictions += count
            else:
                live_predictions += count

    total = float(shots)
    return {
        "live_predictions": live_predictions / total,
        "dud_predictions": dud_predictions / total,
        "detonations": detonations / total,
    }
