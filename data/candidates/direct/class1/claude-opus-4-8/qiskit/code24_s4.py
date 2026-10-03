# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def dj_algorithm(oracle):
    n = oracle.num_qubits - 1

    qc = QuantumCircuit(oracle.num_qubits, n)

    qc.x(n)
    qc.h(range(oracle.num_qubits))

    qc.compose(oracle, inplace=True)

    qc.h(range(n))
    qc.measure(range(n), range(n))

    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1024).result()
    counts = result.get_counts()

    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
