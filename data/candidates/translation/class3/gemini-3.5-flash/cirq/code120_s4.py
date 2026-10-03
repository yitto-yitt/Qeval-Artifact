# EVAL_META: task_id=120, framework=cirq, class=3
import cirq

def create_diagonal_circuit(diag):
    n_qubits = len(diag).bit_length() - 1
    qubits = cirq.LineQubit.range(n_qubits)
    gate = cirq.DiagonalGate(diag)
    return cirq.Circuit(gate.on(*qubits))
