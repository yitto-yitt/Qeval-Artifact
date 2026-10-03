# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    qubits = cirq.LineQubit.range(4)
    custom = cirq.FrozenCircuit(
        cirq.X(qubits[1]),
        cirq.H(qubits[2]),
    )
    controlled_custom = cirq.CircuitOperation(custom).controlled_by(qubits[0], qubits[3])
    return cirq.Circuit(controlled_custom)
