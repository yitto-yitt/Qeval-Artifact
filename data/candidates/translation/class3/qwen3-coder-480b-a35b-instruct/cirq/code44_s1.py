# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    # Create 1-qubit circuit with X gate
    top = cirq.Circuit()
    q0 = cirq.LineQubit(0)
    top.append(cirq.X(q0))
    
    # Create 2-qubit circuit with CRY gate (controlled-Y rotation)
    bottom = cirq.Circuit()
    q1 = cirq.LineQubit(0)  # control qubit
    q2 = cirq.LineQubit(1)  # target qubit
    bottom.append(cirq.ry(0.2).controlled()(q1, q2))
    
    # Tensor product with bottom circuit first (as per requirement)
    # In Cirq, we can achieve this by creating a new circuit and adding moments appropriately
    # We'll create a combined circuit acting on 3 qubits
    combined_qubits = [cirq.LineQubit(i) for i in range(3)]
    combined = cirq.Circuit()
    
    # Add the 2-qubit CRY part first (acting on qubits 0 and 1)
    combined.append(cirq.ry(0.2).controlled()(combined_qubits[0], combined_qubits[1]))
    
    # Add the 1-qubit X gate second (acting on qubit 2)
    combined.append(cirq.X(combined_qubits[2]))
    
    return combined
