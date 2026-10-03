# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit, TranspileConfig, transpile

def create_operator():
    circ = QuantumCircuit(2, 2)
    circ.x(0)
    circ.x(1)
    config = TranspileConfig()
    config.set_optimization_level(1)
    config.set_basis_gates(["U3", "CNOT"])
    return transpile(circ, config)
