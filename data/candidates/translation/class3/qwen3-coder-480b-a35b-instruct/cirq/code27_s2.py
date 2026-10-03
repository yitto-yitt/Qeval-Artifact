# EVAL_META: task_id=27, framework=cirq, class=3
import cirq


def apply_op_back():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H(qubits[0]))
    circuit.append(cirq.CNOT(qubits[0], qubits[1]))
    
    # Convert to list of operations to simulate DAG behavior
    ops = list(circuit.all_operations())
    
    # Apply H gate to qubit 0 at the end (back of the circuit)
    ops.append(cirq.H(qubits[0]))
    
    new_circuit = cirq.Circuit(ops)
    return new_circuit
