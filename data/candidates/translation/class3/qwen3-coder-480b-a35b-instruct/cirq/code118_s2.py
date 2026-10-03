# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = [cirq.LineQubit(i) for i in range(4)]
    circuit = cirq.Circuit()
    
    # C3SX gate is equivalent to a controlled-controlled-controlled-X gate
    c3sx_gate = cirq.X.controlled(num_controls=3)
    circuit.append(c3sx_gate(*qubits))
    
    return circuit
