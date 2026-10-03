# EVAL_META: task_id=92, framework=qpanda2, class=1
from pyqpanda import CPUQVM, QProg, H, CNOT

def calculate_stabilizer_state_info():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    result = qvm.prob_run_dict(prog, qubits, -1)
    prob_dict = {}
    for i, prob in result.items():
        if prob > 1e-12:
            bitstr = format(i, '02b')
            prob_dict[bitstr] = round(prob, 10)
    qvm.finalize()
    return prob_dict
