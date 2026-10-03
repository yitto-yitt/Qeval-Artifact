# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda import *

def remove_unassigned_parameterized_gates(circuit):
    # Create a new circuit to store gates without unassigned parameters
    new_circuit = QCircuit()
    
    # Iterate through all gates in the original circuit
    for gate in circuit.gate_list():
        # Check if the gate has parameters
        if hasattr(gate, 'get_parameter') and gate.get_parameter() is not None:
            # If parameter is assigned (not None), add the gate
            new_circuit.insert(gate)
        elif not hasattr(gate, 'get_parameter'):
            # If gate doesn't have parameters, add it
            new_circuit.insert(gate)
    
    return new_circuit
