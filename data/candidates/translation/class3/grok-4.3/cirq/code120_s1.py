# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import math

def create_diagonal_circuit(diag):
    num_qubits = int(math.log2(len(diag)))
    qubits = cirq.LineQubit.range(num_qubits)
    diagonal_gate = cirq.DiagonalGate(diag)
    circuit = cirq.Circuit(diagonal_gate.on(*qubits))
    return circuit
