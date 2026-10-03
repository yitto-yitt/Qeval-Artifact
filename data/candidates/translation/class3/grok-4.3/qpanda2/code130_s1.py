# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
qubits = machine.qAlloc_many(10)
def inv_circuit(n):
    prog = create_empty_qprog()
    for i in range(2):
        prog << H(qubits[i+1])
    for i in range(2):
        prog << CNOT(qubits[i+1], qubits[i+3])
    return prog.dagger()
machine.finalize()
