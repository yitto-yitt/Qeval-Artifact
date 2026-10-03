# EVAL_META: task_id=125, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)


def circ_to_gate(circ):
    circ_gate = QCircuit()
    circ_gate.insert(circ)
    return circ_gate.to_qgate() if hasattr(circ_gate, "to_qgate") else circ_gate


machine.finalize()
