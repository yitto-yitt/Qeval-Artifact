# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
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
    result = simulator.run(qc, shots=4096).result()
    counts = result.get_counts()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
