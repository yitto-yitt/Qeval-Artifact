# EVAL_META: task_id=99, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
from pyqpanda3.circuit import *

def remove_unassigned_parameterized_gates(circuit):
    # Create a new quantum program without unassigned parameterized gates
    new_prog = QProg()
    
    # Get all gates in the original circuit
    gates = circuit.get_gates()
    
    for gate in gates:
        # Check if the gate has unassigned parameters
        # In pyQPanda3, we need to check if it's a parameterized gate with unassigned parameters
        if hasattr(gate, 'get_parameter') and gate.get_parameter():
            # If it has parameters, we skip it (assuming unassigned)
            continue
        else:
            # Add gate to new program if it doesn't have unassigned parameters
            new_prog.insert(gate)
    
    # Create a new circuit from the program
    new_circuit = QCircuit()
    new_circuit.set_circuit(new_prog)
    
    return new_circuit
