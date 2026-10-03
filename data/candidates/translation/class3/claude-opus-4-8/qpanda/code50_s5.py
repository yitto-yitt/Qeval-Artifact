# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg

def remove_gate_in_position(circuit, position):
    operations = list(circuit)
    del operations[position]
    new_circuit = QCircuit()
    for op in operations:
        new_circuit << op
    return new_circuit
