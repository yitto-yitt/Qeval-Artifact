# EVAL_META: task_id=99, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
from pyqpanda3.extensions import *

def remove_unassigned_parameterized_gates(circuit):
    # Get the number of qubits and classical bits
    qubit_num = len(circuit.get_allocated_qubits())
    cbit_num = len(circuit.get_allocated_cbits())
    
    # Create new circuit without unassigned parameterized gates
    new_circuit = QCircuit()
    qvec = qAlloc_many(qubit_num)
    cvec = cAlloc_many(cbit_num)
    
    # Iterate through the original circuit's instructions
    for gate in circuit.get_gates():
        # Check if the gate has unassigned parameters
        if hasattr(gate, 'get_param'):
            param = gate.get_param()
            # If it's a parameterized gate with unassigned parameters, skip it
            # In pyQPanda3, we check if the parameter is symbolic (unassigned)
            if not isinstance(param, float):  # If parameter is not assigned (not a concrete value)
                continue
        
        # For multi-parameter gates, check each parameter
        elif hasattr(gate, 'get_params'):
            params = gate.get_params()
            skip_gate = False
            for p in params:
                if not isinstance(p, float):  # If any parameter is not assigned
                    skip_gate = True
                    break
            if skip_gate:
                continue
        
        # Add the gate to the new circuit if it doesn't have unassigned parameters
        new_circuit.insert(gate)
    
    return new_circuit
