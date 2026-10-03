# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    sx = cirq.X ** 0.5
    c3sx = sx.controlled(num_controls=3)
    circuit = cirq.Circuit(c3sx(*qubits))
    return circuit
