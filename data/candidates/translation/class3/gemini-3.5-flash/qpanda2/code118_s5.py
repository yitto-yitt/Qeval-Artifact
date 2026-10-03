# EVAL_META: task_id=118, framework=qpanda2, class=3
from pyqpanda import *

# Initialize the global QVM
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)
c = machine.cAlloc_many(4)

def create_c3sx_circuit():
    prog = QProg()
    # Apply SX gate on qubit 3, controlled by qubits 0, 1, and 2
    controlled_sx = SX(q[3]).control([q[0], q[1], q[2]])
    prog.insert(controlled_sx)
    return prog

# Manual Cleanup
machine.finalize()
