# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    gate = (cirq.X**0.5).controlled(3)
    return cirq.Circuit(gate.on(*qubits))
