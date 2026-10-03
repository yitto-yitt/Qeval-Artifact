# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg, H, CNOT, measure_all


def create_ghz(drawing=False):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)

    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << CNOT(qubits[0], qubits[2])
    prog << measure_all(qubits, cbits)

    result = qvm.run_with_configuration(prog, cbits, 1024)

    if drawing:
        return prog, result
    return prog
