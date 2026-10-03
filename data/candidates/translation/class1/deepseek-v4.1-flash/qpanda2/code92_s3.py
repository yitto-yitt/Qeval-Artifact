# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import *

def calculate_stabilizer_state_info():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    machine.run(prog)
    state = machine.get_qstate()
    probs = {}
    for i, amp in enumerate(state):
        p = abs(amp) ** 2
        if p > 1e-12:
            key = format(i, '02b')
            probs[key] = p
    machine.finalize()
    return probs
