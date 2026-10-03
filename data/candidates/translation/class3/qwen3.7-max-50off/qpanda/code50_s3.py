# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_gate_in_position(circuit, position):
    gates = list(circuit)
    del gates[position]
    new_circuit = QCircuit()
    for g in gates:
        new_circuit << g
    return new_circuit
