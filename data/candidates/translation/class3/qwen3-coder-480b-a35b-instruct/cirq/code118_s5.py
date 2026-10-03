# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    
    # C3SX gate is equivalent to a controlled-controlled-controlled-X gate
    # This can be constructed using cirq.X with three controls
    c3sx_gate = cirq.X(*qubits[3:]).controlled_by(*qubits[:3])
    
    circuit.append(c3sx_gate)
    return circuit
