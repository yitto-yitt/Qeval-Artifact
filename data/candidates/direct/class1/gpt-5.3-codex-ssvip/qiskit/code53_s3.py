# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    a = int(a) & 0xFF
    b = int(b) & 0xFF
    x = a ^ b

    qc = QuantumCircuit(8, 8)
    for i in range(8):
        if (x >> i) & 1:
            qc.x(i)
    qc.measure(range(8), range(8))

    simulator = AerSimulator()
    shots = 1024
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)

    probs = {k: v / shots for k, v in counts.items()}
    return probs
