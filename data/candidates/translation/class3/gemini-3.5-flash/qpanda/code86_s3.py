# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT

def collect_linear_blocks_with_and_without_limit():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(5)
    
    # 1. One with no block width restriction (all CX gates in one block)
    prog_full = QProg()
    prog_full.insert(H(q[0]))
    
    block_full = QCircuit()
    block_full.insert(CNOT(q[0], q[1]))
    block_full.insert(CNOT(q[1], q[2]))
    block_full.insert(CNOT(q[2], q[3]))
    block_full.insert(CNOT(q[3], q[4]))
    
    prog_full.insert(block_full)
    
    # 2. One with a max_block_width of 3
    prog_limited = QProg()
    prog_limited.insert(H(q[0]))
    
    block1 = QCircuit()
    block1.insert(CNOT(q[0], q[1]))
    block1.insert(CNOT(q[1], q[2]))
    
    block2 = QCircuit()
    block2.insert(CNOT(q[2], q[3]))
    block2.insert(CNOT(q[3], q[4]))
    
    prog_limited.insert(block1)
    prog_limited.insert(block2)
    
    return prog_full, prog_limited
