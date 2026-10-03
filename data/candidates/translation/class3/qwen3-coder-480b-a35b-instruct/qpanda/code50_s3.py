# EVAL_META: task_id=50, framework=qpanda, class=3
from pyqpanda3.core import *

def remove_gate_in_position(circuit, position):
    # Convert Qiskit circuit to pyQPanda format if needed
    # For this implementation, we assume circuit is already a pyQPanda circuit object
    # Remove the gate at the specified position
    gates = circuit.get_gates()
    new_circuit = QCircuit()
    
    for i, gate in enumerate(gates):
        if i != position:
            new_circuit.insert(gate)
    
    return new_circuit
