# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def or_gate(a, b):
    qc = QuantumCircuit(9, 3)

    # Encode integer a on qubits 0-2 and b on qubits 3-5
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(3 + i)

    # Compute bitwise OR into qubits 6-8
    for i in range(3):
        qc.cx(i, 6 + i)
        qc.cx(3 + i, 6 + i)
        qc.ccx(i, 3 + i, 6 + i)

    # Measure output qubits
    for i in range(3):
        qc.measure(6 + i, i)

    simulator = AerSimulator()
    shots = 1024
    counts = simulator.run(qc, shots=shots).result().get_counts(qc)

    return {bitstring: count / shots for bitstring, count in counts.items()}
