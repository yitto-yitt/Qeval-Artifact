# EVAL_META: task_id=120, framework=cirq, class=3
import numpy as np
import cirq

def create_diagonal_circuit(diag):
    n = int(np.log2(len(diag)))
    gate = cirq.MatrixGate(np.diag(diag), unitary_check=False)
    qubits = cirq.LineQubit.range(n)
    return cirq.Circuit(gate.on(*qubits))
