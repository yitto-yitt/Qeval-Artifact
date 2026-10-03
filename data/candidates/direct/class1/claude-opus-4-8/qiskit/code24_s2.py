# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def dj_algorithm(oracle):
    n = oracle.num_qubits - 1

    qc = QuantumCircuit(n + 1, n)

    qc.x(n)
    qc.h(range(n + 1))

    qc.compose(oracle, qubits=range(n + 1), inplace=True)

    qc.h(range(n))
    qc.measure(range(n), range(n))

    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=1024).result()
    counts = result.get_counts()

    shots = sum(counts.values())
    return {bitstring: count / shots for bitstring, count in counts.items()}
