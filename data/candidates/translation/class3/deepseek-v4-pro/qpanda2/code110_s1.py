# EVAL_META: task_id=110, framework=qpanda2, class=3
import math
import random

import numpy as np
from pyqpanda import *

MAX_QUBITS = 32

machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(MAX_QUBITS)


def _as_prog(circuit):
    if isinstance(circuit, QCircuit):
        prog = QProg()
        prog << circuit
        return prog
    return circuit


def _matrix(circuit):
    return get_matrix(_as_prog(circuit))


def _random_clifford_circuit(num_qubits):
    qc = QCircuit()
    depth = max(10, num_qubits * 10)

    for _ in range(depth):
        gate_type = random.choice(('H', 'S', 'CNOT', 'X', 'Y', 'Z', 'CZ'))
        if gate_type == 'H':
            qc << H(global_qubits[random.randrange(num_qubits)])
        elif gate_type == 'S':
            qc << S(global_qubits[random.randrange(num_qubits)])
        elif gate_type == 'CNOT':
            c = random.randrange(num_qubits)
            t = random.randrange(num_qubits)
            if c != t:
                qc << CNOT(global_qubits[c], global_qubits[t])
        elif gate_type == 'CZ':
            if num_qubits > 1:
                c = random.randrange(num_qubits)
                t = random.randrange(num_qubits)
                if c != t:
                    qc << CZ(global_qubits[c], global_qubits[t])
        else:
            gate = {'X': X, 'Y': Y, 'Z': Z}[gate_type]
            qc << gate(global_qubits[random.randrange(num_qubits)])

    return qc


def equivalent_clifford_circuit(circuit, n):
    target = np.asarray(_matrix(circuit), dtype=complex)
    num_qubits = int(round(math.log2(target.shape[0])))
    qc_list = []
    counter = 0

    while counter < n:
        qc = _random_clifford_circuit(num_qubits)
        mat = np.asarray(_matrix(qc), dtype=complex)
        if np.allclose(mat, target, rtol=0.4, atol=0.4):
            qc_list.append(qc)
            counter += 1

    return qc_list


machine.finalize()
