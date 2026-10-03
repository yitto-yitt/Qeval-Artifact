# EVAL_META: task_id=2, framework=qpanda2, class=2
from pyqpanda import *

def create_bell_statevector():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    machine.directly_run(prog)
    state = machine.get_qstate()
    machine.finalize()
    return state
