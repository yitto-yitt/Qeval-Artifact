# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import random
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits if hasattr(circuit, 'num_qubits') else 2
    used_qubits = qubits[:num_qubits]
    qc_list = []
    counter = 0
    clifford_gates = ['H', 'S', 'X', 'Y', 'Z', 'CZ']
    while counter < n:
        prog = QProg()
        for _ in range(random.randint(5, 15)):
            g = random.choice(clifford_gates)
            if g in ['H', 'S', 'X', 'Y', 'Z']:
                q_idx = random.randint(0, num_qubits-1)
                if g == 'H': prog << H(used_qubits[q_idx])
                elif g == 'S': prog << S(used_qubits[q_idx])
                elif g == 'X': prog << X(used_qubits[q_idx])
                elif g == 'Y': prog << Y(used_qubits[q_idx])
                elif g == 'Z': prog << Z(used_qubits[q_idx])
            elif g == 'CZ' and num_qubits > 1:
                q1, q2 = random.sample(range(num_qubits), 2)
                prog << CZ(used_qubits[q1], used_qubits[q2])
        mat = get_unitary_matrix(prog)
        if hasattr(circuit, 'get_unitary_matrix'):
            mat_or = get_unitary_matrix(circuit)
        else:
            mat_or = np.eye(2**num_qubits, dtype=complex)
        if np.allclose(mat, mat_or, rtol=0.4, atol=0.4):
            counter += 1
            qc_list.append(prog)
    return qc_list
machine.finalize()
