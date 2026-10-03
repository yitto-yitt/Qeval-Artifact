# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    qubits = [cirq.LineQubit(i) for i in range(3)]
    circuit = cirq.Circuit()
    controlled_h = cirq.H.controlled_by(qubits[0], qubits[1])
    circuit.append(controlled_h(*qubits))
    return circuit
