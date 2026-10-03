# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda import *

def remove_gate_in_position(circuit, position):
    # Convert QPanda circuit to list of gates
    gate_list = circuit.get_gates()
    
    # Remove gate at specified position
    if 0 <= position < len(gate_list):
        gate_list.pop(position)
    
    # Create new circuit and add remaining gates
    new_circuit = QCircuit()
    for gate in gate_list:
        new_circuit.insert(gate)
    
    return new_circuit
