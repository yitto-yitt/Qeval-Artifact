from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


def dj_algorithm(oracle):
    if isinstance(oracle, QuantumCircuit):
        n_total = oracle.num_qubits
    elif hasattr(oracle, 'num_qubits'):
        n_total = oracle.num_qubits
    else:
        raise ValueError("Cannot determine oracle qubit count")

    n = n_total - 1  # number of input qubits

    qc = QuantumCircuit(n_total, n)

    # Initialize output qubit (last qubit) to |1>
    qc.x(n)

    # Apply Hadamard to all qubits
    for i in range(n_total):
        qc.h(i)

    # Apply oracle
    if isinstance(oracle, QuantumCircuit):
        if oracle.num_clbits > 0:
            qc.compose(oracle.to_instruction(), qubits=list(range(n_total)), inplace=True)
        else:
            qc.compose(oracle, qubits=list(range(n_total)), inplace=True)
    else:
        qc.append(oracle, list(range(n_total)))

    # Apply Hadamard to input qubits only
    for i in range(n):
        qc.h(i)

    # Measure input qubits
    for i in range(n):
        qc.measure(i, i)

    # Run simulation
    sim = AerSimulator()
    result = sim.run(qc, shots=1024).result()
    counts = result.get_counts()

    # Convert to probability distribution
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
