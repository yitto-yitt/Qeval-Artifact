# EVAL_META: task_id=118, framework=cirq, class=3
import cirq

def create_c3sx_circuit():
    qubits = [cirq.LineQubit(i) for i in range(4)]
    circuit = cirq.Circuit()
    # C3SX gate is equivalent to a controlled-controlled-controlled-X gate
    circuit.append(cirq.TOFFOLI(qubits[0], qubits[1], qubits[2]).controlled_by(qubits[3]))
    # Actually, C3SX is Toffoli with an additional control, so it's a 4-qubit gate
    # We need to decompose it properly - C3SX is CCX with one more control
    circuit = cirq.Circuit()
    # C3SX can be built as a multi-controlled X gate with 3 controls
    mcx = cirq.X.controlled(3)
    circuit.append(mcx(*qubits))
    return circuit
