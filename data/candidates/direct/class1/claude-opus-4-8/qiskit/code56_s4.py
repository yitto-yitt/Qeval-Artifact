# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    n = 8
    bits = format(a & 0xFF, '08b')
    qc = QuantumCircuit(n, n)
    for i, b in enumerate(reversed(bits)):
        if b == '1':
            qc.x(i)
    for i in range(n):
        qc.x(i)
    qc.measure(range(n), range(n))

    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
