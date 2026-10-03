# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    n = 8
    qc = QuantumCircuit(n, n)
    bits = format(a & 0xFF, "08b")
    for i in range(n):
        if bits[n - 1 - i] == "1":
            qc.x(i)
    for i in range(n):
        qc.x(i)
    qc.measure(range(n), range(n))

    sim = AerSimulator()
    shots = 4096
    result = sim.run(qc, shots=shots).result()
    counts = result.get_counts()
    return {k: v / shots for k, v in counts.items()}
