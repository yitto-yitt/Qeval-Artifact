# EVAL_META: task_id=6, framework=cirq, class=2
import cirq

def create_state_prep(num_qubits):
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[0]))
    for q in qubits[1:]:
        circuit.append(cirq.I(q))
    return circuit
