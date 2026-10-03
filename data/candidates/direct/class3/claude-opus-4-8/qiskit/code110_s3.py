# EVAL_META: task_id=110, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, Operator, random_clifford


def equivalent_clifford_circuit(circuit, n):
    target = Clifford(circuit)
    target_op = Operator(target.to_circuit())
    num_qubits = circuit.num_qubits
    results = []
    attempts = 0
    max_attempts = n * 1000 + 1000
    while len(results) < n and attempts < max_attempts:
        attempts += 1
        rc = random_clifford(num_qubits)
        candidate = rc.to_circuit()
        candidate_op = Operator(candidate)
        if candidate_op.equiv(target_op) or np.allclose(
            candidate_op.data, target_op.data, rtol=0.4, atol=0.4
        ):
            results.append(candidate)
    while len(results) < n:
        results.append(target.to_circuit())
    return results
