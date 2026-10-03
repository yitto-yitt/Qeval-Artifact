# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CR, Qubit

def qft_no_swaps(num_qubits):
    qubits = [Qubit(i) for i in range(num_qubits)]
    circuit = QCircuit()
    for j in range(num_qubits):
        q = qubits[j]
        circuit << H(q)
        for k in range(j + 1, num_qubits):
            angle = -3.141592653589793 / (2 ** (k - j))
            circuit << CR(qubits[k], q, angle)
    return circuit
