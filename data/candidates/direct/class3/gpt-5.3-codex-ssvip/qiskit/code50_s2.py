# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit

def remove_gate_in_position(circuit, position):
    if not isinstance(circuit, QuantumCircuit):
        raise TypeError("circuit must be a QuantumCircuit")
    if not isinstance(position, int):
        raise TypeError("position must be an integer")
    if position < 0 or position >= len(circuit.data):
        raise IndexError("position out of range")

    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs, name=circuit.name)
    for i, instruction in enumerate(circuit.data):
        if i != position:
            new_circuit.append(instruction.operation, instruction.qubits, instruction.clbits)
    return new_circuit
