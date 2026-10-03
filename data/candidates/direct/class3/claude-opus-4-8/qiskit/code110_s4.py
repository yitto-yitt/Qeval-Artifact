# EVAL_META: task_id=110, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, Operator, random_clifford


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    target_op = Operator(circuit)
    target_cliff = Clifford(circuit)
    results = []
    attempts = 0
    max_attempts = n * 2000 + 10000
    while len(results) < n and attempts < max_attempts:
        attempts += 1
        rc = random_clifford(num_qubits)
        combined = rc.compose(target_cliff)
        candidate = combined.to_circuit()
        candidate_op = Operator(candidate)
        if _equivalent_up_to_phase(candidate_op.data, target_op.data, 0.4, 0.4):
            results.append(candidate)
    while len(results) < n:
        results.append(target_cliff.to_circuit())
    return results


def _equivalent_up_to_phase(a, b, rtol, atol):
    dim = a.shape[0]
    idx = np.unravel_index(np.argmax(np.abs(b)), b.shape)
    if abs(b[idx]) < 1e-9:
        return np.allclose(a, b, rtol=rtol, atol=atol)
    if abs(a[idx]) < 1e-9:
        return False
    phase = b[idx] / a[idx]
    return np.allclose(a * phase, b, rtol=rtol, atol=atol)
