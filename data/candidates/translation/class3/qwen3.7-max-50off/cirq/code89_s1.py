# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    qubits = cirq.LineQubit.range(3)
    gate = cirq.H.controlled(2)
    return cirq.Circuit(gate.on(*qubits))
