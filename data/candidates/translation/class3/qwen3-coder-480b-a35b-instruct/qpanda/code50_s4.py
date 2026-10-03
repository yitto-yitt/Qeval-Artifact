# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import *

def remove_gate_in_position(circuit, position):
    # Convert position to integer if needed
    pos = int(position)
    
    # Get all gates in the circuit
    gates = circuit.get_gates()
    
    # Create a new circuit
    new_circuit = QCircuit()
    
    # Add all gates except the one at the specified position
    for i, gate in enumerate(gates):
        if i != pos:
            new_circuit.insert(gate)
    
    return new_circuit
