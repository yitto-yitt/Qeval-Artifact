# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    # Define the target operations for the custom gate
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    custom_ops = [cirq.X(qubits[0]), cirq.H(qubits[1])]
    custom_subcircuit = cirq.Circuit(custom_ops)
    
    # Convert to a composite gate
    custom_gate = cirq.CircuitOperation(custom_subcircuit.freeze())
    
    # Create the full circuit with 4 qubits
    full_qubits = [cirq.LineQubit(i) for i in range(4)]
    circuit = cirq.Circuit()
    
    # Apply the custom gate with controls
    controlled_operation = cirq.ControlledGate(
        sub_gate=custom_gate.gate,
        num_controls=2
    ).on(
        full_qubits[0],  # control 1
        full_qubits[3],  # control 2
        full_qubits[1],  # target 1 (for X)
        full_qubits[2]   # target 2 (for H)
    )
    
    # Since the above approach doesn't work directly, we'll manually construct the controlled operation
    circuit.append([
        cirq.Moment([
            cirq.ControlledGate(cirq.X, num_controls=2).on(full_qubits[0], full_qubits[3], full_qubits[1]),
            cirq.ControlledGate(cirq.H, num_controls=2).on(full_qubits[0], full_qubits[3], full_qubits[2])
        ])
    ])
    
    return circuit
