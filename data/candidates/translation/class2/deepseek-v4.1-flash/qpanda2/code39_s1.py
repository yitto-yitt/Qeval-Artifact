# EVAL_META: task_id=39, framework=qpanda2, class=2
from pyqpanda import *

def create_uniform_superposition(n):
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(n)
    prog = QProg()
    for i in range(n):
        prog << H(qubits[i])
    machine.load(prog)
    machine.run()
    state = machine.get_qstate()
    machine.finalize()
    return state
