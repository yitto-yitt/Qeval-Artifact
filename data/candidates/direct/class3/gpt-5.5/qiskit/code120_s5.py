# EVAL_META: task_id=120, framework=qiskit, class=3
from qiskit import QuantumCircuit

try:
    from qiskit.circuit.library import DiagonalGate as _DiagonalGate
except ImportError:
    from qiskit.circuit.library import Diagonal as _DiagonalGate


def create_diagonal_circuit(diag):
    diag = list(diag)
    length = len(diag)
    if length == 0 or length & (length - 1):
        raise ValueError("Length of diag must be a positive power of 2.")

    num_qubits = length.bit_length() - 1
    circuit = QuantumCircuit(num_qubits)
    diagonal = _DiagonalGate(diag)

    if isinstance(diagonal, QuantumCircuit):
        circuit.compose(diagonal, qubits=range(num_qubits), inplace=True)
    else:
        circuit.append(diagonal, range(num_qubits))

    return circuit
