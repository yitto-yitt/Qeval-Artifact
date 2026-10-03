# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def dj_algorithm(oracle):
    num_qubits = oracle.num_qubits
    n = num_qubits - 1
    dj_circuit = QuantumCircuit(num_qubits, n)
    dj_circuit.h(range(n))
    dj_circuit.x(n)
    dj_circuit.h(n)
    dj_circuit.compose(oracle, inplace=True)
    dj_circuit.h(range(n))
    dj_circuit.measure(range(n), range(n))
    backend = AerSimulator()
    transpiled = transpile(dj_circuit, backend)
    job = backend.run(transpiled, shots=1024)
    result = job.result()
    counts = result.get_counts()
    shots = sum(counts.values())
    prob_dist = {bitstring: count / shots for bitstring, count in counts.items()}
    return prob_dist
