# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    c3sx = (cirq.X**0.5).controlled(3)
    circuit.append(c3sx(*qubits))
    return circuit
