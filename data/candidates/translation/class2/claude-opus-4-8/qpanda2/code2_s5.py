# EVAL_META: task_id=2, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QCircuit, H, CNOT


def create_bell_statevector():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)

    prog = QCircuit()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])

    state = qvm.get_qstate(prog)
    qvm.finalize()
    return state
