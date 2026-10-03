# EVAL_META: task_id=125, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QGate

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def circ_to_gate(circ):
    return QGate("circ_gate", circ)

# Manual cleanup
machine.finalize()
