# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT, I


def inv_circuit(n):
    if n < 5:
        raise ValueError("The circuit requires at least five qubits.")

    circuit = QCircuit()
    for qubit in range(n):
        circuit << I(qubit)

    for i in range(2):
        circuit << H(i + 1)

    for i in range(2):
        circuit << CNOT(i + 1, i + 3)

    return circuit.dagger()
