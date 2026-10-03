# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np
import random

def equivalent_clifford_circuit(circuit, n):
    qvm = CPUQVM()
    qvm.init_qvm()
    if hasattr(circuit, 'num_qubits'):
        num_qubits = circuit.num_qubits
    else:
        num_qubits = 2
    qubits = qvm.qAlloc_many(num_qubits)
    op_or = qvm.get_matrix(circuit)
    qc_list = []
    counter = 0
    clifford_gates = ['H', 'S', 'X', 'Y', 'Z', 'CZ', 'CNOT']
    while counter < n:
        qc = QCircuit()
        for _ in range(random.randint(3, 12)):
            g = random.choice(clifford_gates)
            if g in ['H', 'S', 'X', 'Y', 'Z']:
                q_idx = random.randint(0, num_qubits - 1)
                if g == 'H':
                    qc << H(qubits[q_idx])
                elif g == 'S':
                    qc << S(qubits[q_idx])
                elif g == 'X':
                    qc << X(qubits[q_idx])
                elif g == 'Y':
                    qc << Y(qubits[q_idx])
                elif g == 'Z':
                    qc << Z(qubits[q_idx])
            else:
                if num_qubits > 1:
                    q1 = random.randint(0, num_qubits - 1)
                    q2 = random.randint(0, num_qubits - 1)
                    while q2 == q1:
                        q2 = random.randint(0, num_qubits - 1)
                    if g == 'CZ':
                        qc << CZ(qubits[q1], qubits[q2])
                    else:
                        qc << CNOT(qubits[q1], qubits[q2])
        prog = QProg()
        prog << qc
        op_qc = qvm.get_matrix(prog)
        if np.allclose(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    qvm.finalize()
    return qc_list
