# EVAL_META: task_id=125, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QGate

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(16)


def circ_to_gate(circ):
    if isinstance(circ, QCircuit):
        gate = circ.to_qgate() if hasattr(circ, "to_qgate") else circ
        return gate
    if isinstance(circ, QGate):
        return circ
    circ_gate = QCircuit()
    circ_gate.insert(circ)
    return circ_gate


machine.finalize()
