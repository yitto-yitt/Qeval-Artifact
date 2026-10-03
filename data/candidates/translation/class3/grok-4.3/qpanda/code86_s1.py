# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import *

def collect_linear_blocks_with_and_without_limit():
    qm = QuantumMachine()
    qs = qm.allocate_qubits(5)
    circ_full = Circuit()
    circ_full << H(qs[0]) << CNOT(qs[0], qs[1]) << CNOT(qs[1], qs[2]) << CNOT(qs[2], qs[3]) << CNOT(qs[3], qs[4])
    circ_limited = Circuit()
    circ_limited << H(qs[0]) << CNOT(qs[0], qs[1]) << CNOT(qs[1], qs[2])
    circ_limited << CNOT(qs[2], qs[3]) << CNOT(qs[3], qs[4])
    qm.free_qubits(qs)
    return circ_full, circ_limited
