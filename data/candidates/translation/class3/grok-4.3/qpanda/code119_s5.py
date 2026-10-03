# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    machine = init_quantum_machine(QuantumMachineType.CPU)
    if kind == 'full':
        n_qubits = 2 * num_state_qubits + 2
    elif kind == 'half':
        n_qubits = 2 * num_state_qubits + 1
    else:
        n_qubits = 2 * num_state_qubits + 1
    qvec = machine.qAlloc_many(n_qubits)
    prog = QProg()
    for i in range(num_state_qubits):
        prog << CNOT(qvec[i], qvec[num_state_qubits + i])
        prog << Toffoli(qvec[i], qvec[num_state_qubits + i], qvec[n_qubits - 1])
    for i in range(num_state_qubits - 1, -1, -1):
        prog << CNOT(qvec[i], qvec[num_state_qubits + i])
    machine.finalize()
    return prog
