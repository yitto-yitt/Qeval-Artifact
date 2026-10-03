# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda3.core import *

def controlled_custom_unitary_circuit():
    init_quantum_machine(QMachineType.CPU)
    qubits = qAlloc_many(2)
    prog = QProg()
    gate = U3(qubits[1], 0.3, 0.2, 0.1)
    prog << gate.control([qubits[0]])
    return prog
