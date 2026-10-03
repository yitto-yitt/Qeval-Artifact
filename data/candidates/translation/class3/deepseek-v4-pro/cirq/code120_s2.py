# EVAL_META: task_id=120, framework=cirq, class=3
import numpy as np
import cirq


def create_diagonal_circuit(diag):
    """Create a Cirq circuit applying a diagonal gate."""
    dim = len(diag)
    num_qubits = int(np.log2(dim))
    gate = cirq.MatrixGate(np.diag(diag))
    qubits = cirq.LineQubit.range(num_qubits)
    return cirq.Circuit(gate.on(*qubits))
