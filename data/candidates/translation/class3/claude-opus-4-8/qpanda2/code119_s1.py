# EVAL_META: task_id=119, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == "half":
        total_qubits = 2 * num_state_qubits
    elif kind == "full":
        total_qubits = 2 * num_state_qubits + 1
    elif kind == "fixed":
        total_qubits = 2 * num_state_qubits
    else:
        raise ValueError(f"Unknown kind: {kind}")
    
    qubits = machine.qAlloc_many(total_qubits)
    prog = QProg()
    
    for i in range(num_state_qubits):
        a_qubit = qubits[i]
        b_qubit = qubits[num_state_qubits + i]
        
        if i == 0:
            if kind == "half":
                prog << CNOT(a_qubit, b_qubit)
                prog << CNOT(b_qubit, a_qubit)
                prog << CNOT(a_qubit, b_qubit)
            elif kind == "full":
                c_in = qubits[2 * num_state_qubits]
                prog << CNOT(a_qubit, b_qubit)
                prog << CNOT(a_qubit, c_in)
                prog << Toffoli(b_qubit, c_in, a_qubit)
            elif kind == "fixed":
                prog << CNOT(a_qubit, b_qubit)
        else:
            c = qubits[num_state_qubits + i - 1] if kind != "full" else qubits[2 * num_state_qubits]
            prog << CNOT(a_qubit, b_qubit)
            prog << CNOT(a_qubit, c)
            prog << Toffoli(b_qubit, c, a_qubit)
    
    return prog

machine.finalize()
