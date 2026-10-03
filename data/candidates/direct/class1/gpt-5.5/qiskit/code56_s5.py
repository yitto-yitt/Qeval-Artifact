# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def not_gate(a):
    a = int(a) & 0xFF

    qc = QuantumCircuit(8, 8)

    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)

    for i in range(8):
        qc.x(i)

    qc.measure(range(8), range(8))

    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    shots = 1024
    counts = simulator.run(compiled, shots=shots).result().get_counts()

    return {format(int(bitstring.replace(" ", ""), 2), "08b"): count / shots for bitstring, count in counts.items()}
