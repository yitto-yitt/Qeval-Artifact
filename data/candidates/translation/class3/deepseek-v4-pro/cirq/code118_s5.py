# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    circuit.append(cirq.X.controlled(3).on(*qubits[:3]).with_tags(cirq.Tag.TO_CIRQ_REVERSE_TAG))
    
    # This needs to be a C3SX gate (Sqrt(X) controlled by 3 qubits)
    # Cirq doesn't have C3SX natively, so we decompose using C3X and SX
    q0, q1, q2, q3 = qubits
    circuit = cirq.Circuit()
    circuit.append(cirq.X.controlled(3).on(q0, q1, q2, q3)**0.5)
    
    return circuit
