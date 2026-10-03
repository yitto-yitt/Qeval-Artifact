# EVAL_META: task_id=90, framework=cirq, class=3
import cirq

def create_custom_controlled():
    qubits = cirq.LineQubit.range(4)
    q0, q1 = cirq.LineQubit.range(2)
    base_circuit = cirq.Circuit(cirq.X(q0), cirq.H(q1))
    base_op = cirq.CircuitOperation(base_circuit.freeze())
    controlled_op = base_op.on(qubits[1], qubits[2]).controlled_by(qubits[0], qubits[3])
    circuit = cirq.Circuit(controlled_op)
    return circuit
