# EVAL_META: task_id=119, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(30)
def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == 'full':
        total_qubits = 2 * num_state_qubits + 2
    elif kind == 'half':
        total_qubits = 2 * num_state_qubits + 1
    else:
        total_qubits = 2 * num_state_qubits
    prog = QProg()
    for i in range(num_state_qubits):
        prog << CNOT(qubits[i], qubits[num_state_qubits + i])
        if i < num_state_qubits - 1 or kind == 'full':
            prog << Toffoli(qubits[i], qubits[num_state_qubits + i], qubits[2 * num_state_qubits])
    if kind == 'full':
        prog << CNOT(qubits[2 * num_state_qubits], qubits[2 * num_state_qubits + 1])
    return prog
machine.finalize()
