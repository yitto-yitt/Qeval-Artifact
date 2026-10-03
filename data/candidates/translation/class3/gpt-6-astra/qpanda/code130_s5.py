# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CNOT, I

def inv_circuit(n):
    if n < 5:
        raise ValueError("The circuit requires at least five qubits.")

    circuit = QCircuit()
    for i in range(n):
        circuit << I(i)
    circuit << H(1)
    circuit << H(2)
    circuit << CNOT(1, 3)
    circuit << CNOT(2, 4)
    return circuit.dagger()
