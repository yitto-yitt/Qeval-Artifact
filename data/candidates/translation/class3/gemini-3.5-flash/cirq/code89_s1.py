# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    c2h = cirq.H.controlled(2)
    circuit.append(c2h(*qubits))
    return circuit
