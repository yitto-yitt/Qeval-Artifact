# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
pool_qubits = machine.qAlloc_many(20)

def _equiv_up_to_phase(U, V, rtol=0.4, atol=0.4):
    dim = U.shape[0]
    inner = np.trace(U.conj().T @ V)
    if abs(inner) < 1e-10:
        return False
    phase = inner / dim
    phase = phase / abs(phase)
    return np.allclose(U, phase * V, rtol=rtol, atol=atol)

def _random_clifford_circuit(qubits):
    circ = QCircuit()
    num_qubits = len(qubits)
    num_gates = 20 * num_qubits
    for _ in range(num_gates):
        gate_type = random.choice(['H', 'S', 'X', 'Y', 'Z', 'CNOT'])
        if gate_type == 'CNOT':
            q1, q2 = random.sample(qubits, 2)
            circ << CNOT(q1, q2)
        else:
            q = random.choice(qubits)
            if gate_type == 'H':
                circ << H(q)
            elif gate_type == 'S':
                circ << S(q)
            elif gate_type == 'X':
                circ << X(q)
            elif gate_type == 'Y':
                circ << Y(q)
            elif gate_type == 'Z':
                circ << Z(q)
    return circ

def equivalent_clifford_circuit(circuit, n):
    qubits_used = circuit.get_qubits()
    if not isinstance(qubits_used, list):
        qubits_used = list(qubits_used)
    
    U_orig = circuit.get_matrix()
    
    result = []
    while len(result) < n:
        rand_circ = _random_clifford_circuit(qubits_used)
        U_rand = rand_circ.get_matrix()
        if _equiv_up_to_phase(U_orig, U_rand, rtol=0.4, atol=0.4):
            result.append(rand_circ)
    return result

machine.finalize()
