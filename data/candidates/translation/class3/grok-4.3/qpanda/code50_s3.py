# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QuantumCircuit

def remove_gate_in_position(circuit, position):
    del circuit.data[position]
    return circuit
