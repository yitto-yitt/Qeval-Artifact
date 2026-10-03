# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    machine = init_quantum_machine(QMachineType.CPU)
    if kind == 'half':
        n_qubits = 2 * num_state_qubits + 1
    elif kind == 'fixed':
        n_qubits = 2 * num_state_qubits
    else:
        n_qubits = 2 * num_state_qubits + 2
    qubits = machine.qAlloc_many(n_qubits)
    prog = QProg()
    circuit = QCircuit()
    for i in range(num_state_qubits):
        circuit << CNOT(qubits[i], qubits[num_state_qubits + i])
        if i < num_state_qubits - 1 or kind == 'full':
            circuit << Toffoli(qubits[i], qubits[num_state_qubits + i], qubits[n_qubits - 1])
            if i < num_state_qubits - 1:
                circuit << CNOT(qubits[num_state_qubits + i], qubits[i + 1])
    prog << circuit
    return prog
