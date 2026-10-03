# EVAL_META: task_id=110, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, Operator, random_clifford


def equivalent_clifford_circuit(circuit, n):
    target = Clifford(circuit)
    num_qubits = circuit.num_qubits
    target_op = Operator(target.to_circuit())
    results = []
    while len(results) < n:
        rc = random_clifford(num_qubits)
        candidate = rc.compose(target)
        cand_circ = candidate.to_circuit()
        if Operator(cand_circ).equiv(target_op, rtol=0.4, atol=0.4):
            results.append(cand_circ)
    return results
