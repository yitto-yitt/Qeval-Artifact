# EVAL_META: task_id=50, framework=qiskit, class=3

from qiskit import QuantumCircuit

def remove_gate_in_position(circuit, position):
    # Create a new quantum circuit with the same registers as the input circuit
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    
    # Iterate through the instructions in the original circuit
    for i, instruction in enumerate(circuit.data):
        # Skip the instruction at the specified position
        if i != position:
            # Add the instruction to the new circuit
            new_circuit.append(instruction.operation, instruction.qubits, instruction.clbits)
    
    return new_circuit
