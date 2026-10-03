# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    n = 8
    qc = QuantumCircuit(n, n)

    # Initialize qubits to represent the 8-bit integer a
    for i in range(n):
        if (a >> i) & 1:
            qc.x(i)

    # Apply bitwise NOT (X gate to all qubits)
    for i in range(n):
        qc.x(i)

    # Measure all qubits
    for i in range(n):
        qc.measure(i, i)

    # Simulate
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert to probability distribution with 8-bit keys
    total = sum(counts.values())
    probs = {}
    for key, count in counts.items():
        # Ensure 8-bit string format
        bitstring = key.replace(" ", "").zfill(n)
        probs[bitstring] = count / total

    return probs
