# EVAL_META: task_id=90, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QProg, QCircuit, X, H

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)


def create_custom_controlled():
    custom = QCircuit()
    custom << X(qubits[1])
    custom << H(qubits[2])
    custom.set_control([qubits[0], qubits[3]])

    program = QProg()
    program << custom
    machine.directly_run(program)
    return program


atexit.register(lambda: machine.finalize())
