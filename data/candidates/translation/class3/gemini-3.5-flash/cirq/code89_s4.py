# EVAL_META: task_id=89, framework=cirq, class=3
import cirq

def create_controlled_hgate():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    cc_h = cirq.H.controlled(num_controls=2)
    circuit.append(cc_h(*qubits))
    return circuit
