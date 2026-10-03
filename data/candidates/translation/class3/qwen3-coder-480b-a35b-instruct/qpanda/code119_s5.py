# EVAL_META: task_id=119, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
from pyqpanda3.algorithm import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    # Create quantum program and machine
    prog = QProg()
    qvm = CPUQVM()
    qvm.init_qvm()
    
    # Calculate total number of qubits needed
    # For ripple carry adder: 2*num_state_qubits + 1 (for carry) + num_state_qubits (for output)
    total_qubits = 2 * num_state_qubits + 1 + num_state_qubits
    qubits = qvm.qAlloc_many(total_qubits)
    
    # In pyQPanda3, we need to manually implement the ripple carry adder logic
    # Using the built-in Adder implementation
    if kind == 'full':
        # Full adder - includes carry input and carry output
        prog << adder(qubits[:num_state_qubits], 
                     qubits[num_state_qubits:2*num_state_qubits], 
                     qubits[2*num_state_qubits], 
                     qubits[2*num_state_qubits+1:2*num_state_qubits+1+num_state_qubits])
    elif kind == 'half':
        # Half adder - no initial carry input
        prog << half_adder(qubits[:num_state_qubits], 
                          qubits[num_state_qubits:2*num_state_qubits], 
                          qubits[2*num_state_qubits], 
                          qubits[2*num_state_qubits+1:2*num_state_qubits+1+num_state_qubits])
    else:  # fixed or default
        prog << adder(qubits[:num_state_qubits], 
                     qubits[num_state_qubits:2*num_state_qubits], 
                     qubits[2*num_state_qubits], 
                     qubits[2*num_state_qubits+1:2*num_state_qubits+1+num_state_qubits])
    
    return prog
