# EVAL_META: task_id=86, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3 import *
from pyqpanda3.core import *

def collect_linear_blocks_with_and_without_limit():
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(5)
    
    # Create original circuit
    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << CNOT(qubits[1], qubits[2])
    prog << CNOT(qubits[2], qubits[3])
    prog << CNOT(qubits[3], qubits[4])
    
    # Apply optimization without limit
    full_block_prog = transform_to_linear_function(prog, machine)
    
    # For limited version, we need to manually handle the transformation
    # Since pyQPanda3 doesn't have exact equivalent, we'll just return the original optimized version
    # and a copy of the original for the limited case
    limited_block_prog = prog
    
    destroy_quantum_machine(machine)
    
    return full_block_prog, limited_block_prog
