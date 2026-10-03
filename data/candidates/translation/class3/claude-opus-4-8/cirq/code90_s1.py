# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    qubits = cirq.LineQubit.range(4)
    sub_ops = [cirq.X(cirq.LineQubit(0)), cirq.H(cirq.LineQubit(1))]
    custom_gate = cirq.CircuitOperation(
        cirq.FrozenCircuit(sub_ops)
    ).controlled_by(qubits[0], qubits[3])
    mapped = custom_gate.with_qubit_mapping({
        cirq.LineQubit(0): qubits[1],
        cirq.LineQubit(1): qubits[2],
    })
    circuit = cirq.Circuit()
    circuit.append(mapped)
    return circuit
