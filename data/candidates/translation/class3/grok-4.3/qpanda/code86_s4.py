# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import *
def collect_linear_blocks_with_and_without_limit():
    machine = QuantumMachine()
    q = machine.allocate_qubits(5)
    prog = QProg()
    prog.insert(H(q[0])).insert(CNOT(q[0], q[1])).insert(CNOT(q[1], q[2])).insert(CNOT(q[2], q[3])).insert(CNOT(q[3], q[4]))
    full_block = prog
    limited_block = QProg()
    limited_block.insert(H(q[0])).insert(CNOT(q[0], q[1])).insert(CNOT(q[1], q[2]))
    limited_block.insert(CNOT(q[2], q[3])).insert(CNOT(q[3], q[4]))
    return full_block, limited_block
