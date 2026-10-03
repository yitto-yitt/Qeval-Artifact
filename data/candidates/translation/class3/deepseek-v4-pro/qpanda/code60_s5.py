# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_cy_gate():
    circuit = QuantumCircuit(2)
    circuit.sdg(1)
    circuit.cx(0, 1)
    circuit.s(1)
    return circuit
