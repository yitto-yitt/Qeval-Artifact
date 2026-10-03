# EVAL_META: task_id=120, framework=cirq, class=3
import cirq

def create_diagonal_circuit(diag):
    gate = cirq.DiagonalGate(diag)
    qubits = cirq.LineQubit.range(gate.num_qubits())
    return cirq.Circuit(gate.on(*qubits))
