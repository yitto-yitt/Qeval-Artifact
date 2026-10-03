# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    a_int = int(a)
    b_int = int(b)
    if not (0 <= a_int <= 255 and 0 <= b_int <= 255):
        raise ValueError("a and b must be 8-bit integers in [0, 255].")

    xor_val = a_int ^ b_int
    qc = QuantumCircuit(8, 8)

    for i in range(8):
        if (xor_val >> i) & 1:
            qc.x(i)

    qc.measure(range(8), range(8))

    sim = AerSimulator()
    shots = 1024
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts(qc)

    probs = {k: v / shots for k, v in counts.items()}
    return probs
