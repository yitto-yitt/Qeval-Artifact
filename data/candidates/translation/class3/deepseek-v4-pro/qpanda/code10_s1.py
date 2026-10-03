# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, Operator, transpile

def create_operator():
    XX = Operator([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    circ = QuantumCircuit(2, 2)
    circ.append(XX, [0, 1])
    transpiled_circ = transpile(circ, optimization_level=1, basis_gates=["u", "cx"])
    return transpiled_circ
