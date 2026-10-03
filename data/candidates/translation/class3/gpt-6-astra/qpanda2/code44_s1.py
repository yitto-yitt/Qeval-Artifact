# EVAL_META: task_id=44, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, RY, X

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(machine.finalize)


def tensor_circuits():
    top = QCircuit()
    top << X(qubits[0])

    bottom = QCircuit()
    bottom << RY(qubits[2], 0.2).control([qubits[1]])

    tensored = QCircuit()
    tensored << bottom << top

    program = QProg()
    program << tensored
    machine.directly_run(program)
    return tensored
