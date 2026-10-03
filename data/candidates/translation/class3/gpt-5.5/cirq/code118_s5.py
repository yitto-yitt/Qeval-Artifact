# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = cirq.LineQubit.range(4)
    circuit = cirq.Circuit()
    circuit.append((cirq.X(qubits[3]) ** 0.5).controlled_by(qubits[0], qubits[1], qubits[2]))
    return circuit
