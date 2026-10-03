# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    ch_gate = cirq.H.controlled(2)
    circuit.append(ch_gate.on(*qubits))
    return circuit
