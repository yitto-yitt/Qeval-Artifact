# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    # Create the base 2-qubit gate with X on qubit 0 and H on qubit 1
    q0, q1 = cirq.LineQubit.range(2)
    base_circuit = cirq.Circuit()
    base_circuit.append(cirq.X(q0))
    base_circuit.append(cirq.H(q1))
    
    # Convert to a custom gate
    custom_gate = cirq.CircuitOperation(base_circuit.freeze()).repeat(1)
    
    # Create a controlled version with 2 control qubits
    # In Cirq, we'll manually implement the controlled behavior
    controls = cirq.LineQubit.range(2, 4)  # qubits 2, 3 as controls
    targets = [q0, q1]  # qubits 0, 1 as targets
    
    # Create the full 4-qubit circuit
    all_qubits = cirq.LineQubit.range(4)
    full_circuit = cirq.Circuit()
    
    # Apply controlled operations
    # Control the X gate on q0 with both control qubits
    full_circuit.append(cirq.X(q0).controlled_by(controls[0], controls[1]))
    # Control the H gate on q1 with both control qubits
    full_circuit.append(cirq.H(q1).controlled_by(controls[0], controls[1]))
    
    return full_circuit
