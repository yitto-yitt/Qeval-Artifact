# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import *

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    qvm.run(prog)
    state = qvm.get_qstate()
    probs = {}
    for i in range(len(state)):
        p = abs(state[i]) ** 2
        if p > 1e-12:
            bitstring = format(i, '02b')[::-1]
            probs[bitstring] = p
    qvm.finalize()
    return probs
