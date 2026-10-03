# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    a_int = int(a) & 0xFF
    bitstr = format(a_int, "08b")

    qc = QuantumCircuit(8, 8)

    for i, b in enumerate(reversed(bitstr)):
        if b == "1":
            qc.x(i)

    for i in range(8):
        qc.x(i)

    qc.measure(range(8), range(8))

    simulator = AerSimulator()
    shots = 1024
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts(qc)

    return {k: v / shots for k, v in counts.items()}
