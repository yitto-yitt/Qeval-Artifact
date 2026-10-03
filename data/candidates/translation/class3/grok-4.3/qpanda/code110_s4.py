# EVAL_META: task_id=110, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    num_qubits = getattr(circuit, 'num_qubits', 2)
    qc_list = []
    counter = 0
    machine = CPUQVM()
    machine.init_qvm()
    while counter < n:
        q = machine.qAlloc_many(num_qubits)
        prog = QProg()
        for i in range(num_qubits):
            if np.random.rand() > 0.5:
                prog << H(q[i])
            if np.random.rand() > 0.5:
                prog << S(q[i])
        for i in range(num_qubits - 1):
            if np.random.rand() > 0.5:
                prog << CNOT(q[i], q[i + 1])
        qc_list.append(prog)
        counter += 1
    machine.finalize()
    return qc_list
