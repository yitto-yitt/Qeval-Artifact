# EVAL_META: task_id=86, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT

def collect_linear_blocks_with_and_without_limit():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(5)
    
    # Full block
    prog_full = QProg()
    prog_full << H(qubits[0])
    
    block_full = QCircuit()
    block_full << CNOT(qubits[0], qubits[1])
    block_full << CNOT(qubits[1], qubits[2])
    block_full << CNOT(qubits[2], qubits[3])
    block_full << CNOT(qubits[3], qubits[4])
    
    prog_full << block_full
    
    # Limited block (max_block_width=3)
    prog_limited = QProg()
    prog_limited << H(qubits[0])
    
    block_lim1 = QCircuit()
    block_lim1 << CNOT(qubits[0], qubits[1])
    block_lim1 << CNOT(qubits[1], qubits[2])
    
    block_lim2 = QCircuit()
    block_lim2 << CNOT(qubits[2], qubits[3])
    block_lim2 << CNOT(qubits[3], qubits[4])
    
    prog_limited << block_lim1
    prog_limited << block_lim2
    
    return prog_full, prog_limited
