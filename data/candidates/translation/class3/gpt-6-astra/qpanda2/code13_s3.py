# EVAL_META: task_id=13, framework=qpanda2, class=3
import atexit
from math import pi
from pyqpanda import CPUQVM, QCircuit, QProg, U3

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def custom_rotation_gate():
    circuit = QCircuit()
    circuit << U3(qubits[0], pi / 2, pi / 2, pi / 2)
    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(lambda: machine.finalize())
