# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def dj_algorithm(oracle):
    if isinstance(oracle, QuantumCircuit):
        num_qubits = oracle.num_qubits
    elif hasattr(oracle, 'num_qubits'):
        num_qubits = oracle.num_qubits
    else:
        raise ValueError("Unknown oracle type")

    n = num_qubits - 1  # number of input qubits

    qc = QuantumCircuit(num_qubits, n)

    # Set output qubit (last qubit) to |1>
    qc.x(n)

    # Apply Hadamard to all qubits
    for i in range(num_qubits):
        qc.h(i)

    # Apply oracle
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

    # Run on simulator
    sim = AerSimulator()
    transpiled = transpile(qc, sim)
    result = sim.run(transpiled, shots=1024).result()
    counts = result.get_counts()

    # Convert counts to probability distribution
    total = sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    return probs
