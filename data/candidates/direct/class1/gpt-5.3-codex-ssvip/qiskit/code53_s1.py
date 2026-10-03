# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    a = int(a) & 0xFF
    b = int(b) & 0xFF

    qc = QuantumCircuit(8, 8)

    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(i)

    qc.measure(range(8), range(8))

    simulator = AerSimulator()
    shots = 1024
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)

    dist = {format(i, "08b"): 0.0 for i in range(256)}
    for bitstr, cnt in counts.items():
        dist[bitstr] = cnt / shots
    return dist
