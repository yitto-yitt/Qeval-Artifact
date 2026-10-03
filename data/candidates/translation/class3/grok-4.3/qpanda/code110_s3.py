# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    op_or = get_unitary(circuit)
    qc_list = []
    counter = 0
    while counter < n:
        qc = _random_clifford_circuit(num_qubits)
        op_qc = get_unitary(qc)
        if np.allclose(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list

def _random_clifford_circuit(num_qubits):
    qvm = CPUQVM()
    qvm.init_qvm()
    qvec = qvm.qAlloc_many(num_qubits)
    qc = QCircuit()
    for _ in range(20):
        g = np.random.choice(['H', 'S', 'CX', 'CZ'])
        if g == 'H':
            q = np.random.randint(num_qubits)
            qc << H(qvec[q])
        elif g == 'S':
            q = np.random.randint(num_qubits)
            qc << S(qvec[q])
        elif g == 'CX':
            q1, q2 = np.random.choice(num_qubits, 2, replace=False)
            qc << CNOT(qvec[q1], qvec[q2])
        else:
            q1, q2 = np.random.choice(num_qubits, 2, replace=False)
            qc << CZ(qvec[q1], qvec[q2])
    qvm.finalize()
    return qc
