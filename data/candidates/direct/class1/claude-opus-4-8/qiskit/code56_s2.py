# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    bits = format(a & 0xFF, "08b")
    qc = QuantumCircuit(8, 8)
    for i, b in enumerate(reversed(bits)):
        if b == "1":
            qc.x(i)
    qc.x(range(8))
    qc.measure(range(8), range(8))

    sim = AerSimulator()
    shots = 4096
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()
    return {k: v / shots for k, v in counts.items()}
