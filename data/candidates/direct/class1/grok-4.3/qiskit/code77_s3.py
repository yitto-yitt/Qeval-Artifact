# EVAL_META: task_id=77, framework=qiskit, class=1
import math
from qiskit import QuantumCircuit

def circuit_from_probability_dist(probability_dist):
    if not probability_dist:
        qc = QuantumCircuit(1)
        qc.measure_all()
        return qc
    bitstrings = list(probability_dist.keys())
    n_qubits = len(bitstrings[0])
    num_states = 2 ** n_qubits
    statevector = [0.0] * num_states
    for bitstring, prob in probability_dist.items():
        index = int(bitstring, 2)
        statevector[index] = math.sqrt(float(prob))
    qc = QuantumCircuit(n_qubits)
    qc.initialize(statevector, range(n_qubits))
    qc.measure_all()
    return qc
