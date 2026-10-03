# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import numpy as np

def create_diagonal_circuit(diag):
    diagonal_gate = cirq.MatrixGate(np.diag(np.asarray(diag, dtype=complex)))
    qubits = cirq.LineQubit.range(cirq.num_qubits(diagonal_gate))
    return cirq.Circuit(diagonal_gate.on(*reversed(qubits)))
