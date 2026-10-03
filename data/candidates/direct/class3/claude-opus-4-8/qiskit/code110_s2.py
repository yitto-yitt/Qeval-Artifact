# EVAL_META: task_id=110, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, Operator, random_clifford


def equivalent_clifford_circuit(circuit, n):
    target = Clifford(circuit)
    num_qubits = circuit.num_qubits
    target_op = Operator(target.to_circuit())
    result = []
    attempts = 0
    max_attempts = n * 2000 + 10000
    while len(result) < n and attempts < max_attempts:
        attempts += 1
        rand = random_clifford(num_qubits)
        candidate = rand.to_circuit()
        if Operator(candidate).equiv(target_op, rtol=0.4, atol=0.4):
            result.append(candidate)
    while len(result) < n:
        result.append(target.to_circuit())
    return result
