# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def dj_algorithm(oracle):
    """Build and run the Deutsch-Jozsa routine for a given oracle.

    The oracle is expected to act on ``n + 1`` qubits where the final qubit
    is the output (target) qubit.  The returned dictionary maps measured
    input-register bitstrings to probabilities.
    """
    num_qubits = oracle.num_qubits
    n = num_qubits - 1

    qc = QuantumCircuit(num_qubits, n)

    # Prepare the output qubit in |-> and the input register in |+>^n.
    qc.x(n)
    qc.h(range(num_qubits))

    # Apply the oracle.
    qc.compose(oracle, inplace=True)

    # Interfere the input register.
    qc.h(range(n))

    # Measure only the input register.
    qc.measure(range(n), range(n))

    simulator = AerSimulator()
    transpiled = transpile(qc, simulator)
    result = simulator.run(transpiled, shots=4096).result()
    counts = result.get_counts()

    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
