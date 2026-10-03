# EVAL_META: task_id=110, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
import random
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)
def equivalent_clifford_circuit(circuit, n):
    num_qubits = 2
    try:
        used = circuit.get_used_qubits()
        num_qubits = len(used)
    except:
        pass
    op_or = get_unitary(circuit, [qubits[i] for i in range(num_qubits)])
    qc_list = []
    counter = 0
    while counter < n:
        prog = QProg()
        for _ in range(random.randint(3, 12)):
            q1 = random.randint(0, num_qubits-1)
            q2 = random.randint(0, num_qubits-1)
            g = random.choice([0,1,2])
            if g == 0:
                prog << H(qubits[q1])
            elif g == 1:
                prog << S(qubits[q1])
            elif g == 2 and q1 != q2:
                prog << CNOT(qubits[q1], qubits[q2])
        try:
            op_qc = get_unitary(prog, [qubits[i] for i in range(num_qubits)])
            diff = np.min([np.linalg.norm(op_qc - op_or), np.linalg.norm(op_qc + op_or)])
            if diff < 0.4 * np.sqrt(op_or.size):
                counter += 1
                qc_list.append(prog)
        except:
            pass
    return qc_list
machine.finalize()
