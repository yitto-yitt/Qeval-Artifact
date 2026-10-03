# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def simple_elitzur_vaidman():
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cnot(0, 1)
    circuit.h(0)
    return circuit
