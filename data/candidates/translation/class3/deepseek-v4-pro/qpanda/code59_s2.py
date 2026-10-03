# EVAL_META: task_id=59, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def create_cz_gate():
    circuit = QuantumCircuit(2)
    circuit.h(1)
    circuit.cx(0, 1)
    circuit.h(1)
    return circuit
