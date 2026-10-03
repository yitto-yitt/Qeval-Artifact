# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def or_gate(a, b):
    a = int(a)
    b = int(b)
    if not (0 <= a <= 7 and 0 <= b <= 7):
        raise ValueError("a and b must be 3-bit integers in the range 0..7")

    qc = QuantumCircuit(9, 3)

    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(3 + i)

    for i in range(3):
        qc.cx(i, 6 + i)
        qc.cx(3 + i, 6 + i)
        qc.ccx(i, 3 + i, 6 + i)

    for i in range(3):
        qc.measure(6 + i, i)

    shots = 1024
    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=shots).result()
    counts = result.get_counts()

    return {key: value / shots for key, value in counts.items()}
