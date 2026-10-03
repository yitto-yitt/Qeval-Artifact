# EVAL_META: task_id=6, framework=qpanda2, class=2
from pyqpanda import *


def create_state_prep(num_qubits):
    try:
        q = qAlloc_many(num_qubits)
    except:
        init_quantum_machine(QuantumMachine_Type.CPU)
        q = qAlloc_many(num_qubits)

    prog = QProg()
    prog << X(q[0])
    return prog
