# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    a = int(a) & 0xFF
    n = 8
    shots = 1024

    qc = QuantumCircuit(n, n)

    for i in range(n):
        if (a >> i) & 1:
            qc.x(i)

    for i in range(n):
        qc.x(i)

    qc.measure(range(n), range(n))

    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)

    return {format(int(bitstr.replace(" ", ""), 2), "08b"): count / shots for bitstr, count in counts.items()}
