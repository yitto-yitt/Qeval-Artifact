# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import *


def calculate_stabilizer_state_info():
    qvm = CPUQVM()

    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    if hasattr(qvm, "qAlloc_many"):
        qubits = qvm.qAlloc_many(2)
    elif hasattr(qvm, "qalloc_many"):
        qubits = qvm.qalloc_many(2)
    else:
        qubits = [qvm.qAlloc(), qvm.qAlloc()]

    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])

    if hasattr(qvm, "prob_run_dict"):
        result = qvm.prob_run_dict(prog, qubits, -1)
    elif hasattr(qvm, "prob_run_tuple_list"):
        result = dict(qvm.prob_run_tuple_list(prog, qubits, -1))
    elif hasattr(qvm, "get_prob_dict"):
        if hasattr(qvm, "directly_run"):
            qvm.directly_run(prog)
        elif hasattr(qvm, "run"):
            qvm.run(prog)
        result = qvm.get_prob_dict(qubits)
    else:
        result = dict(qvm.prob_run(prog, qubits))

    if hasattr(qvm, "finalize"):
        qvm.finalize()
    elif hasattr(qvm, "finalize_qvm"):
        qvm.finalize_qvm()

    return {str(k): float(v) for k, v in result.items() if abs(float(v)) > 1e-15}
