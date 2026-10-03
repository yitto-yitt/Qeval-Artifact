# EVAL_META: task_id=86, framework=qpanda2, class=3
from pyqpanda import *

# Global QVM Initialization
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(5)

def collect_linear_blocks_with_and_without_limit():
    # Full block (no limit)
    # The entire CX chain is collected into one block (width 5)
    prog_full = QProg()
    prog_full << H(q[0])
    
    block_full = QCircuit()
    block_full << CX(q[0], q[1]) \
               << CX(q[1], q[2]) \
               << CX(q[2], q[3]) \
               << CX(q[3], q[4])
    prog_full << block_full
    
    # Limited block (max_block_width = 3)
    # The CX chain is split into blocks of width <= 3
    # Block 1: CX(0,1), CX(1,2) -> qubits {0, 1, 2} (width 3)
    # Block 2: CX(2,3), CX(3,4) -> qubits {2, 3, 4} (width 3)
    prog_limited = QProg()
    prog_limited << H(q[0])
    
    block_lim1 = QCircuit()
    block_lim1 << CX(q[0], q[1]) \
               << CX(q[1], q[2])
               
    block_lim2 = QCircuit()
    block_lim2 << CX(q[2], q[3]) \
               << CX(q[3], q[4])
               
    prog_limited << block_lim1 << block_lim2
    
    return prog_full, prog_limited

# Manual Cleanup
machine.finalize()
