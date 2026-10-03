# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np
machine = pq.CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    controls = [qubits[0], qubits[1], qubits[2]]
    target = qubits[3]
    prog << pq.U3(target, np.pi/2, -np.pi/2, np.pi/2).control(controls)
    return prog

machine.finalize()
