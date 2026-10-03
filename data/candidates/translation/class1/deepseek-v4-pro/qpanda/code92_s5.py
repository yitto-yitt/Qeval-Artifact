# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import (
    init_quantum_machine,
    destroy_quantum_machine,
    QMachineType,
    qAlloc_many,
    QProg,
    H,
    CNOT,
    prob_run_dict,
)

def calculate_stabilizer_state_info():
    init_quantum_machine(QMachineType.CPU)
    try:
        q = qAlloc_many(2)
        prog = QProg()
        prog << H(q[0]) << CNOT(q[0], q[1])

        probabilities = prob_run_dict(prog, q)

        for state in [format(i, '02b') for i in range(4)]:
            probabilities.setdefault(state, 0.0)

        return probabilities
    finally:
        destroy_quantum_machine()
