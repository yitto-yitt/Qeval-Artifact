# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    circuit = cirq.Circuit()
    qubits = cirq.LineQubit.range(4)
    c3sx_gate = cirq.ControlledGate(cirq.SX, num_controls=3)
    circuit.append(c3sx_gate.on(*qubits))
    return circuit
