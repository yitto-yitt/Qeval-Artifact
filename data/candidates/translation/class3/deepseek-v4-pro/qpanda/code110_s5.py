# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np
import random

def _to_prog(circ):
    if isinstance(circ, QCircuit):
        prog = QProg()
        prog << circ
        return prog
    return circ

def _get_matrix(circ, qubits):
    prog = _to_prog(circ)
    try:
        mat = np.asarray(get_matrix(prog, qubits))
    except NameError:
        qvm = CPUQVM()
        mat = np.asarray(qvm.get_matrix(prog, qubits))
    if mat.ndim == 1:
        dim = 2 ** len(qubits)
        mat = mat.reshape(dim, dim)
    return mat

def _is_equiv(a, b, rtol=0.4, atol=0.4):
    if a.shape != b.shape:
        return False
    trace = np.trace(a.conj().T @ b)
    if abs(trace) == 0:
        return False
    phase = trace / abs(trace)
    return np.allclose(a, phase * b, rtol=rtol, atol=atol)

def _random_clifford_circuit(qubits, num_qubits):
    circ = QCircuit()
    depth = max(20, 20 * num_qubits)
    for _ in range(depth):
        r = random.random()
        if r < 0.55:
            q = qubits[random.randrange(num_qubits)]
            circ << H(q)
        elif r < 0.75:
            q = qubits[random.randrange(num_qubits)]
            circ << S(q)
        else:
            if num_qubits < 2:
                q = qubits[random.randrange(num_qubits)]
                circ << S(q)
            else:
                c = random.randrange(num_qubits)
                t = random.randrange(num_qubits)
                while t == c:
                    t = random.randrange(num_qubits)
                circ << CNOT(qubits[c], qubits[t])
    return circ

def equivalent_clifford_circuit(circuit, n):
    qubits = list(get_used_qubits(circuit))
    num_qubits = len(qubits)
    op_original = _get_matrix(circuit, qubits)
    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(qubits, num_qubits)
        op_qc = _get_matrix(qc, qubits)
        if _is_equiv(op_original, op_qc):
            counter += 1
            qc_list.append(qc)
    return qc_list
