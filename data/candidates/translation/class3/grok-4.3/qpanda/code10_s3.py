# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QGateFactory, optimize_circuit

def create_operator():
    XX = [[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]
    circ = QCircuit(2)
    gate = QGateFactory.create_unitary_gate(XX)
    circ.append(gate, [0, 1])
    return optimize_circuit(circ, optimization_level=1, basis_gates=["u", "cx"])
