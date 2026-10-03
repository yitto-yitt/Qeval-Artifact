# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import *
def collect_linear_blocks_with_and_without_limit():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(5)
    prog_full = create_empty_circuit()
    prog_full << H(q[0]) << CNOT(q[0], q[1]) << CNOT(q[1], q[2]) << CNOT(q[2], q[3]) << CNOT(q[3], q[4])
    prog_limited = create_empty_circuit()
    prog_limited << H(q[0]) << CNOT(q[0], q[1]) << CNOT(q[1], q[2]) << CNOT(q[2], q[3]) << CNOT(q[3], q[4])
    return prog_full, prog_limited
