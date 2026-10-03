# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def dj_algorithm(oracle):
    num_qubits = oracle.num_qubits
    n = num_qubits - 1  # number of input qubits

    qc = QuantumCircuit(num_qubits, n)

    # Put output qubit (last qubit) into |-> state
    qc.x(num_qubits - 1)

    # Apply Hadamard to all qubits
    for i in range(num_qubits):
        qc.h(i)

    # Apply the oracle
    if isinstance(oracle, QuantumCircuit):
        qc.compose(oracle, inplace=True)
    else:
        qc.append(oracle, list(range(num_qubits)))

    # Apply Hadamard to input qubits only
    for i in range(n):
        qc.h(i)

    # Measure input qubits
    for i in range(n):
        qc.measure(i, i)

    # Run on Aer simulator
    sim = AerSimulator()
    qc_t = transpile(qc, sim)
    result = sim.run(qc_t, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total_shots = sum(counts.values())
    probs = {bitstring: count / total_shots for bitstring, count in counts.items()}

    return probs
