# EVAL_META: task_id=125, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import CPUQVM, qAlloc_many

# Global QVM and qubit allocation
machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(10)

def circ_to_gate(circ):
    return pq.circuit_to_gate(circ)

# Manual cleanup
machine.finalize()
