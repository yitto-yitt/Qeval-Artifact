# EVAL_META: task_id=120, framework=cirq, class=3
import cirq

def create_diagonal_circuit(diag):
    n = (len(diag).bit_length() - 1)
    qubits = cirq.LineQubit.range(n)
    size = len(diag)
    mat = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        mat[i][i] = diag[i]
    gate = cirq.MatrixGate(mat)
    circuit = cirq.Circuit(gate(*qubits))
    return circuit
