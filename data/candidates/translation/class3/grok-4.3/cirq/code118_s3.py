# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    c3sx = cirq.ControlledGate(cirq.SX, num_controls=3)
    circuit = cirq.Circuit(c3sx.on(*qubits))
    return circuit
