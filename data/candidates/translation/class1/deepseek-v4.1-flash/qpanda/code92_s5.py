# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    qvm.run(prog)
    state = qvm.get_qstate()
    probabilities = {}
    n = 2
    for i, amp in enumerate(state):
        prob = abs(amp) ** 2
        if prob > 1e-12:
            bitstring = format(i, f'0{n}b')
            probabilities[bitstring] = prob
    return probabilities
