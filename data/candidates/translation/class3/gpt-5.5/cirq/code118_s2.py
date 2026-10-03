# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    c3sx_gate = cirq.ControlledGate(cirq.X**0.5, num_controls=3)
    circuit = cirq.Circuit(c3sx_gate.on(qubits[0], qubits[1], qubits[2], qubits[3]))
    return circuit
