# EVAL_META: task_id=120, framework=cirq, class=3
import cirq

def create_diagonal_circuit(diag):
    n = len(diag).bit_length() - 1
    qubits = cirq.LineQubit.range(n)
    gate = cirq.DiagonalGate(diag)
    qc = cirq.Circuit(gate.on(*qubits))
    return qc
