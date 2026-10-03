# EVAL_META: task_id=44, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg, X, RY

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def tensor_circuits():
    try:
        top = QCircuit()
        top << X(qubits[0])

        bottom = QCircuit()
        bottom << RY(qubits[2], 0.2).control([qubits[1]])

        tensored = QCircuit()
        tensored << top << bottom

        program = QProg()
        program << tensored
        machine.directly_run(program)
        return tensored
    finally:
        machine.finalize()
