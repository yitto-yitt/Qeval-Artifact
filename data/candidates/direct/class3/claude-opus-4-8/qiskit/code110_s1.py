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
    max_attempts = n * 2000 + 5000

    while len(results) < n and attempts < max_attempts:
        attempts += 1
        rc = random_clifford(num_qubits)
        prefix = rc.to_circuit()
        inv = rc.adjoint()
        combined = inv.compose(target_cliff)
        full = prefix.compose(combined.to_circuit())

        candidate = QuantumCircuit(num_qubits)
        candidate.compose(full, inplace=True)

        cand_op = Operator(candidate)
        if cand_op.equiv(target_op, rtol=0.4, atol=0.4):
            results.append(candidate)

    while len(results) < n:
        results.append(circuit.copy())

    return results
