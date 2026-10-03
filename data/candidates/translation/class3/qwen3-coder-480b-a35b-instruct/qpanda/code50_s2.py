# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import *

def remove_gate_in_position(circuit, position):
    # Convert position to zero-based index
    pos = int(position)
    
    # Get all gates in the circuit
    gates = circuit.get_gates()
    
    # Create a new circuit without the gate at the specified position
    new_circuit = QCircuit()
    
    for i, gate in enumerate(gates):
        if i != pos:
            new_circuit.insert(gate)
    
    return new_circuit
