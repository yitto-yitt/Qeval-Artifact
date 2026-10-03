# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    # Create the custom gate with X on qubit 0 and H on qubit 1
    qubits_2 = [cirq.LineQubit(0), cirq.LineQubit(1)]
    custom_circuit = cirq.Circuit()
    custom_circuit.append(cirq.X(qubits_2[0]))
    custom_circuit.append(cirq.H(qubits_2[1]))
    
    # Convert to a composite gate
    custom_operation = cirq.CircuitOperation(custom_circuit.freeze())
    
    # Create the main circuit with 4 qubits
    qubits_4 = [cirq.LineQubit(i) for i in range(4)]
    main_circuit = cirq.Circuit()
    
    # Create a controlled version of the custom operation
    # Controls are on qubits 0 and 3, targets are on qubits 1 and 2
    controlled_op = custom_operation.with_tags(cirq.VirtualTag()).controlled_by(
        qubits_4[0], qubits_4[3]
    )
    
    # To properly map the controlled operation, we need to remap the target qubits
    # The original custom operation acts on qubits 0,1 - we need it to act on qubits 1,2
    mapped_op = controlled_op.transform_qubits([qubits_4[0], qubits_4[3], qubits_4[1], qubits_4[2]])
    
    main_circuit.append(mapped_op)
    
    return main_circuit
