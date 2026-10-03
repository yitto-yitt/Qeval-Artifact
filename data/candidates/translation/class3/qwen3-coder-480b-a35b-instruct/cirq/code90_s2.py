# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    # Define the operations for the custom gate
    def custom_ops(qubits):
        yield cirq.X(qubits[0])
        yield cirq.H(qubits[1])
    
    # Create the base operation
    qubits_2d = [cirq.LineQubit(0), cirq.LineQubit(1)]
    base_op = cirq.Circuit(custom_ops(qubits_2d)).to_op()
    
    # Create the controlled version with 2 control qubits
    control_qubits = [cirq.LineQubit(2), cirq.LineQubit(3)]
    target_qubits = [cirq.LineQubit(0), cirq.LineQubit(1)]
    
    # Create the controlled operation
    controlled_op = cirq.ControlledOperation(control_qubits, 
                                           cirq.CircuitOperation(cirq.FrozenCircuit(
                                               cirq.X(target_qubits[0]),
                                               cirq.H(target_qubits[1])
                                           ).as_composite_circuit()))
    
    # Actually we need to build it differently since cirq handles controlled ops differently
    x_on_ctrl = cirq.X(target_qubits[0]).controlled_by(*control_qubits)
    h_on_ctrl = cirq.H(target_qubits[1]).controlled_by(*control_qubits)
    
    # Create the full circuit
    circuit = cirq.Circuit()
    all_qubits = [cirq.LineQubit(i) for i in range(4)]
    circuit.append([x_on_ctrl, h_on_ctrl])
    
    return circuit
