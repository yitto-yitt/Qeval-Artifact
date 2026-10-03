# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import QCircuit

def remove_gate_in_position(circuit, position):
    gates = list(circuit.get_gates())
    del gates[position]
    new_circuit = QCircuit()
    for gate in gates:
        new_circuit << gate
    return new_circuit
