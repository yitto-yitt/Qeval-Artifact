# EVAL_META: task_id=11, framework=qpanda2, class=2
from pyqpanda import *

def get_statevector(circuit):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = circuit.get_qubits()
    if qubits:
        num_qubits = max(q.get_index() for q in qubits) + 1
    else:
        num_qubits = 0
    new_qubits = qvm.qAlloc_many(num_qubits)
    prog = QProg()
    prog << circuit
    qvm.direct_run(prog, new_qubits, 1)
    return qvm.get_qstate()
