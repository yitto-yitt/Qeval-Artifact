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
        total_qubits = 2 * num_state_qubits + 1
    else:
        total_qubits = 2 * num_state_qubits + 2
    
    qubits = machine.qAlloc_many(total_qubits)
    prog = QProg()
    
    a_qubits = qubits[:num_state_qubits]
    b_qubits = qubits[num_state_qubits:2*num_state_qubits]
    
    if kind == 'half':
        carry_qubits = qubits[2*num_state_qubits:2*num_state_qubits+1]
        for i in range(num_state_qubits - 1):
            prog << CNOT(a_qubits[i], b_qubits[i])
            prog << CNOT(a_qubits[i], carry_qubits[0])
            prog << Toffoli(b_qubits[i], carry_qubits[0], a_qubits[i+1] if i+1 < num_state_qubits else carry_qubits[0])
        if num_state_qubits > 0:
            prog << CNOT(a_qubits[-1], b_qubits[-1])
    elif kind == 'full':
        cin = qubits[2*num_state_qubits]
        cout = qubits[2*num_state_qubits+1]
        carry = cin
        for i in range(num_state_qubits):
            prog << CNOT(a_qubits[i], b_qubits[i])
            prog << CNOT(a_qubits[i], carry)
            if i < num_state_qubits - 1:
                prog << Toffoli(b_qubits[i], carry, a_qubits[i+1])
            else:
                prog << Toffoli(b_qubits[i], carry, cout)
    elif kind == 'fixed':
        carry_qubits = qubits[2*num_state_qubits:2*num_state_qubits+1]
        for i in range(num_state_qubits):
            prog << CNOT(a_qubits[i], b_qubits[i])
            if i < num_state_qubits - 1:
                prog << Toffoli(a_qubits[i], b_qubits[i], a_qubits[i+1])
    
    return prog

machine.finalize()
