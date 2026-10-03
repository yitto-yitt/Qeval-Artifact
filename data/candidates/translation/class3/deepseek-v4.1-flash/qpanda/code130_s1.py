# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H, CNOT

def inv_circuit(n):
    q = [Qubit(i) for i in range(n)]
    circuit = QCircuit()
    circuit << CNOT(q[2], q[4])
    circuit << CNOT(q[1], q[3])
    circuit << H(q[2])
    circuit << H(q[1])
    return circuit
