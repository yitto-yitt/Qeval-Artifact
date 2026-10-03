# EVAL_META: task_id=59, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
def create_cz_gate():
    circuit = create_empty_circuit()
    circuit << H(q[1]) << CNOT(q[0], q[1]) << H(q[1])
    return circuit
machine.finalize()
