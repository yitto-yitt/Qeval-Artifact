# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3.core import init_quantum_machine, QMachineType, create_empty_qprog, H, CNOT, get_unitary_matrix


def get_unitary():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(2)
    prog = create_empty_qprog()
    prog << H(q[0]) << CNOT(q[0], q[1])
    return get_unitary_matrix(prog, machine)
