# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QProg, gate

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    machine = QuantumMachine()
    if kind == 'full':
        total_qubits = 2 * num_state_qubits + 2
    elif kind == 'half':
        total_qubits = 2 * num_state_qubits + 1
    else:
        total_qubits = 2 * num_state_qubits + 1
    qubits = machine.allocate_qubits(total_qubits)
    prog = QProg(machine)
    for i in range(num_state_qubits):
        prog.insert(gate.CNOT(qubits[i], qubits[num_state_qubits + i]))
        if i < num_state_qubits - 1 or kind == 'full':
            prog.insert(gate.Toffoli(qubits[i], qubits[num_state_qubits + i], qubits[total_qubits - 1]))
            prog.insert(gate.CNOT(qubits[total_qubits - 1], qubits[i + 1]))
    return prog
