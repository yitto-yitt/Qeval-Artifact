# EVAL_META: task_id=120, framework=cirq, class=3
import cirq

def create_diagonal_circuit(diag):
    diagonal_gate = cirq.DiagonalGate(diag)
    num_qubits = diagonal_gate.num_qubits
    qc = cirq.Circuit(diagonal_gate.on(*cirq.LineQubit.range(num_qubits)))
    return qc
