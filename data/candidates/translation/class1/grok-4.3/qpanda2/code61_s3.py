# EVAL_META: task_id=61, framework=qpanda2, class=1
from pyqpanda import init_quantum_machine, QMachineType, create_empty_qprog, measure


def create_quantum_circuit_with_one_qubit_and_measure():
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)
    prog = create_empty_qprog()
    prog << measure(q[0], c[0])
    return prog
