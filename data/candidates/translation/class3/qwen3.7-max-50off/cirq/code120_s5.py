# EVAL_META: task_id=120, framework=cirq, class=3
import cirq
import math

def create_diagonal_circuit(diag):
    n = int(math.log2(len(diag)))
    qubits = cirq.LineQubit.range(n)
    gate = cirq.DiagonalGate(diag)
    circuit = cirq.Circuit(gate(*qubits))
    return circuit
