# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def dj_algorithm(oracle):
    n_total = oracle.num_qubits
    n = n_total - 1  # number of input qubits (last qubit is output)

    qc = QuantumCircuit(n_total, n)

    # Initialize output qubit to |1>
    qc.x(n)

    # Apply Hadamard to all qubits
    for i in range(n_total):
        qc.h(i)

    # Apply the oracle
    qc.compose(oracle, inplace=True)

    # Apply Hadamard to input qubits only
    for i in range(n):
        qc.h(i)

    # Measure input qubits
    for i in range(n):
        qc.measure(i, i)

    # Simulate
    sim = AerSimulator()
    transpiled = transpile(qc, sim)
    result = sim.run(transpiled, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total = sum(counts.values())
    probs = {bitstring: count / total for bitstring, count in counts.items()}

    return probs
