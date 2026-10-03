# EVAL_META: task_id=86, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit
from pyqpanda3.algorithms import *

def collect_linear_blocks_with_and_without_limit():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = [machine.qAlloc() for _ in range(5)]
    
    prog = QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.CNOT(qubits[1], qubits[2])
    prog << pq.CNOT(qubits[2], qubits[3])
    prog << pq.CNOT(qubits[3], qubits[4])
    
    # Apply transformation without limit
    full_block_prog = pq.transform_to_linear(prog, -1)  # -1 indicates no limit
    
    # Apply transformation with limit of 3
    limited_block_prog = pq.transform_to_linear(prog, 3)
    
    pq.destroy_quantum_machine(machine)
    
    return full_block_prog, limited_block_prog
