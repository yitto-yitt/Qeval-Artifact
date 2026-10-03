# EVAL_META: task_id=110, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(5)
def equivalent_clifford_circuit(circuit, n):
    prog_or = QProg()
    prog_or << circuit
    op_or = get_unitary_matrix(prog_or)
    num_qubits = len(qubits)
    qc_list = []
    counter = 0
    while counter < n:
        qc = QCircuit()
        for _ in range(20):
            g = np.random.choice(['H','S','X','Y','Z','CNOT','CZ'])
            if g in ['H','S','X','Y','Z']:
                q = np.random.randint(0, num_qubits)
                if g == 'H': qc << H(qubits[q])
                elif g == 'S': qc << S(qubits[q])
                elif g == 'X': qc << X(qubits[q])
                elif g == 'Y': qc << Y(qubits[q])
                elif g == 'Z': qc << Z(qubits[q])
            else:
                q1 = np.random.randint(0, num_qubits)
                q2 = np.random.randint(0, num_qubits)
                while q2 == q1: q2 = np.random.randint(0, num_qubits)
                if g == 'CNOT': qc << CNOT(qubits[q1], qubits[q2])
                else: qc << CZ(qubits[q1], qubits[q2])
        prog_qc = QProg()
        prog_qc << qc
        op_qc = get_unitary_matrix(prog_qc)
        if np.allclose(op_qc, op_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(qc)
    return qc_list
machine.finalize()
