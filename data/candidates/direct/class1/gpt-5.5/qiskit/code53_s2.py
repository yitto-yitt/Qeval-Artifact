# EVAL_META: task_id=53, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def xor_gate(a, b):
    a = int(a) & 0xFF
    b = int(b) & 0xFF

    qc = QuantumCircuit(16, 8)

    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(8 + i)

    for i in range(8):
        qc.cx(i, 8 + i)
        qc.measure(8 + i, i)

    shots = 1024
    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=shots).result()
    counts = result.get_counts()

    return {format(int(k.replace(" ", ""), 2), "08b"): v / shots for k, v in counts.items()}
