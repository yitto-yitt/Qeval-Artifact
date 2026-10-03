# EVAL_META: task_id=125, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(1)


def circ_to_gate(circ):
    try:
        return circuit_to_gate(circ)
    except Exception:
        circ_gate = QCircuit()
        circ_gate.insert(circ)
        return circ_gate


atexit.register(machine.finalize)
