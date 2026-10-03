# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def dj_algorithm(oracle):
    n = oracle.num_qubits - 1
    qc = QuantumCircuit(n + 1)
    qc.x(n)
    qc.h(range(n + 1))
    qc.compose(oracle, inplace=True)
    qc.h(range(n))
    sv = Statevector(qc)
    probs_full = sv.probabilities_dict()
    probs = {}
    for state, prob in probs_full.items():
        input_bits = state[1:]  # drop ancilla (first char)
        probs[input_bits] = probs.get(input_bits, 0.0) + prob
    return probs
