from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def not_gate(a):
    n = 8
    qc = QuantumCircuit(n, n)

    # Initialize qubits to represent the binary value of a
    for i in range(n):
        if (a >> i) & 1:
            qc.x(i)

    # Apply NOT (X gate) to all qubits
    for i in range(n):
        qc.x(i)

    # Measure all qubits
    for i in range(n):
        qc.measure(i, i)

    # Simulate
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert to probability distribution
    total = sum(counts.values())
    probs = {}
    for key, val in counts.items():
        formatted_key = key.zfill(n)
        probs[formatted_key] = val / total

    return probs
