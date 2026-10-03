# EVAL_META: task_id=125, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)


def circ_to_gate(circ):
    circ_gate = QCircuit(circ)
    return circ_gate.to_gate() if hasattr(circ_gate, "to_gate") else circ_gate


machine.finalize()
