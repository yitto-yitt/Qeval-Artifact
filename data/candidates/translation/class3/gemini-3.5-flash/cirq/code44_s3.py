# EVAL_META: task_id=44, framework=cirq, class=3
import cirq

def tensor_circuits():
    qubits = cirq.LineQubit.range(3)
    circuit = cirq.Circuit()
    circuit.append(cirq.X(qubits[0]))
    circuit.append(cirq.ry(0.2).on(qubits[2]).controlled_by(qubits[1]))
    return circuit
