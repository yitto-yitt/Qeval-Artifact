# EVAL_META: task_id=119, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == 'half':
        total_qubits = 2 * num_state_qubits + 1
    elif kind == 'full':
        total_qubits = 2 * num_state_qubits + 2
    elif kind == 'fixed':
        total_qubits = 2 * num_state_qubits
    else:
        raise ValueError(f"Invalid kind: {kind}")
    
    qubits = machine.qAlloc_many(total_qubits)
    prog = QProg()
    
    a_qubits = qubits[:num_state_qubits]
    b_qubits = qubits[num_state_qubits:2*num_state_qubits]
    
    if kind == 'half':
        carry_qubits = qubits[2*num_state_qubits:]
        
        for i in range(num_state_qubits - 1):
            prog << CNOT(a_qubits[i], carry_qubits[i]) \
                 << CNOT(b_qubits[i], carry_qubits[i]) \
                 << Toffoli(a_qubits[i], b_qubits[i], carry_qubits[i+1]) \
                 << CNOT(a_qubits[i], carry_qubits[i+1]) \
                 << CNOT(b_qubits[i], carry_qubits[i+1])
        
        prog << CNOT(a_qubits[-1], b_qubits[-1]) \
             << CNOT(carry_qubits[-2], b_qubits[-1])
        
        for i in range(num_state_qubits - 2, -1, -1):
            prog << Toffoli(a_qubits[i], b_qubits[i], carry_qubits[i+1]) \
                 << CNOT(a_qubits[i], carry_qubits[i+1]) \
                 << CNOT(b_qubits[i], carry_qubits[i+1]) \
                 << CNOT(a_qubits[i], b_qubits[i]) \
                 << CNOT(carry_qubits[i], b_qubits[i])
                
    elif kind == 'full':
        carry_in = qubits[2*num_state_qubits]
        carry_qubits = qubits[2*num_state_qubits+1:]
        
        prog << CNOT(a_qubits[0], b_qubits[0]) \
             << CNOT(carry_in, b_qubits[0])
        
        for i in range(num_state_qubits - 1):
            prog << Toffoli(a_qubits[i], b_qubits[i], carry_qubits[i]) \
                 << CNOT(a_qubits[i], carry_qubits[i]) \
                 << CNOT(b_qubits[i], carry_qubits[i])
            
            if i == 0:
                prog << Toffoli(carry_in, b_qubits[i], carry_qubits[i])
                prog << CNOT(carry_in, carry_qubits[i])
        
        prog << CNOT(a_qubits[-1], b_qubits[-1]) \
             << CNOT(carry_qubits[-1], b_qubits[-1])
        
        for i in range(num_state_qubits - 2, -1, -1):
            if i == 0:
                prog << Toffoli(carry_in, b_qubits[i], carry_qubits[i])
                prog << CNOT(carry_in, carry_qubits[i])
            
            prog << Toffoli(a_qubits[i], b_qubits[i], carry_qubits[i]) \
                 << CNOT(a_qubits[i], carry_qubits[i]) \
                 << CNOT(b_qubits[i], carry_qubits[i]) \
                 << CNOT(a_qubits[i], b_qubits[i])
            
            if i > 0:
                prog << CNOT(carry_qubits[i-1], b_qubits[i])
            else:
                prog << CNOT(carry_in, b_qubits[i])
                
    elif kind == 'fixed':
        for i in range(num_state_qubits - 1):
            prog << Toffoli(a_qubits[i], b_qubits[i], a_qubits[i+1]) \
                 << CNOT(a_qubits[i], b_qubits[i])
        
        prog << CNOT(a_qubits[-1], b_qubits[-1])
        
        for i in range(num_state_qubits - 2, -1, -1):
            prog << CNOT(a_qubits[i], b_qubits[i]) \
                 << Toffoli(a_qubits[i], b_qubits[i], a_qubits[i+1]) \
                 << CNOT(a_qubits[i], b_qubits[i]) \
                 << CNOT(a_qubits[i+1], b_qubits[i])
    
    return prog

machine.finalize()
