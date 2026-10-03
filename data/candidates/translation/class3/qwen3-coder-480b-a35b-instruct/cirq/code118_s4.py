# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = [cirq.LineQubit(i) for i in range(4)]
    circuit = cirq.Circuit()
    # C3SX gate is equivalent to a controlled-controlled-controlled-X gate (Toffoli-like with 3 controls)
    c3sx_gate = cirq.ControlledGate(cirq.ControlledGate(cirq.ControlledGate(cirq.X), num_controls=1), num_controls=2)
    circuit.append(c3sx_gate(*qubits))
    return circuit
