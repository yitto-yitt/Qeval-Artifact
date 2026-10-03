# EVAL_META: task_id=78, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
def qft_no_swaps(num_qubits):
    q = qubits[:num_qubits]
    circuit = create_empty_circuit()
    for target in range(num_qubits-1, -1, -1):
        for control in range(num_qubits-1, target, -1):
            angle = -np.pi / 2**(control - target)
            circuit << CR(q[control], q[target], angle)
        circuit << H(q[target])
    return circuit
machine.finalize()
