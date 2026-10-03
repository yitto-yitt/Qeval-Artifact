# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    qubits = cirq.LineQubit.range(3)
    ch_gate = cirq.H.controlled(2)
    circuit = cirq.Circuit(ch_gate(qubits[0], qubits[1], qubits[2]))
    return circuit
