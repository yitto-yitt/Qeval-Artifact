# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    # Create the custom operation (X on qubit 0, H on qubit 1)
    qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    custom_op = cirq.Circuit([
        cirq.X(qubits[0]),
        cirq.H(qubits[1])
    ]).to_op()
    
    # Create 4 qubits for the main circuit
    main_qubits = [cirq.LineQubit(i) for i in range(4)]
    
    # Create a controlled version of the custom operation with 2 control qubits
    # Controls are on qubits 0 and 3, targets are on qubits 1 and 2
    controlled_custom = cirq.ControlledOperation(
        controls=[main_qubits[0], main_qubits[3]], 
        sub_operation=cirq.Circuit([
            cirq.X(main_qubits[1]),
            cirq.H(main_qubits[2])
        ]).to_op()
    )
    
    # Create the main circuit and append the controlled operation
    circuit = cirq.Circuit()
    circuit.append(controlled_custom)
    
    return circuit
