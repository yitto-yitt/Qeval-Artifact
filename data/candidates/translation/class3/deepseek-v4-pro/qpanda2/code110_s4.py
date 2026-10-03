# EVAL_META: task_id=110, framework=qpanda2, class=3
import random
import numpy as np
from pyqpanda import *

_QVM = CPUQVM()
_QVM.initQVM()

def _get_circuit_matrix(prog):
    return np.asarray(getCircuitMatrix(prog), dtype=complex)

def _random_clifford_sequence(qubits):
    qubits = list(qubits)
    num_qubits = len(qubits)
    prog = QProg()
    gates = []
    depth = 20 * num_qubits + 5
    for _ in range(depth):
        r = random.random()
        if num_qubits >= 2 and r < 0.25:
            c = random.randrange(num_qubits)
            t = random.randrange(num_qubits)
            while t == c:
                t = random.randrange(num_qubits)
            gate = CNOT(qubits[c], qubits[t])
        elif r < 0.70:
            gate = H(qubits[random.randrange(num_qubits)])
        else:
            gate = S(qubits[random.randrange(num_qubits)])
        gates.append(gate)
        prog << gate
    return prog, gates

def _inverse_sequence(gates):
    inv = QProg()
    for gate in reversed(gates):
        inv << gate.dagger()
    return inv

def _operator_equiv(op1, op2, rtol=0.4, atol=0.4):
    if op1.shape != op2.shape:
        return False
    dim = op1.shape[0]
    phase = np.vdot(op1, op2) / dim
    if abs(phase) > 0:
        op2 = op2 * (phase / abs(phase))
    return bool(np.allclose(op1, op2, rtol=rtol, atol=atol))

def equivalent_clifford_circuit(circuit, n):
    base = QProg()
    base << circuit
    qubits = list(base.get_used_qubits())
    op_or = _get_circuit_matrix(base)
    qc_list = []
    counter = 0
    while counter < n:
        seq, gates = _random_clifford_sequence(qubits)
        inv = _inverse_sequence(gates)
        candidate = QProg()
        candidate << base << seq << inv
        op_candidate = _get_circuit_matrix(candidate)
        if _operator_equiv(op_or, op_candidate):
            counter += 1
            qc_list.append(candidate)
    return qc_list

_QVM.finalize()
