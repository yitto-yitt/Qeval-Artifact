# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, CPUQVM


def create_swap_gate():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)

    circuit = QCircuit()
    circuit << qvm.CX(q[0], q[1])
    circuit << qvm.CX(q[1], q[0])
    circuit << qvm.CX(q[0], q[1])

    prog = QProg()
    prog << circuit
    qvm.directly_run(prog)

    return circuit
