# EVAL_META: task_id=50, framework=qiskit, class=3
from qiskit import QuantumCircuit


def remove_gate_in_position(circuit, position):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    for i, instruction in enumerate(circuit.data):
        if i != position:
            new_circuit.append(instruction.operation, instruction.qubits, instruction.clbits)
    return new_circuit
