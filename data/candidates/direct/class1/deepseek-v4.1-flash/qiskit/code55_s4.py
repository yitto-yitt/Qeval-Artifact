# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def or_gate(a, b):
    result = (int(a) | int(b)) & 0b111
    qc = QuantumCircuit(3, 3)
    for i in range(3):
        if (result >> i) & 1:
            qc.x(i)
    qc.measure([0, 1, 2], [0, 1, 2])
    shots = 1024
    backend = AerSimulator()
    counts = backend.run(qc, shots=shots).result().get_counts()
    return {k: v / shots for k, v in counts.items()}
