# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    qubits = cirq.LineQubit.range(3)
    c3h_gate = cirq.H.controlled(2)
    circuit = cirq.Circuit(c3h_gate(*qubits))
    return circuit
