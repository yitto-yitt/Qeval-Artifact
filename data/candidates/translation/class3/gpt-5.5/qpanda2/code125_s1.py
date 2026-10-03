# EVAL_META: task_id=125, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(64)
atexit.register(machine.finalize)


def circ_to_gate(circ):
    circ_gate = QCircuit()
    circ_gate.insert(circ)
    return circ_gate
