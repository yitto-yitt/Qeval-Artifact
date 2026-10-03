# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import QProg, QCircuit, QGate, Parameter
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def remove_unassigned_parameterized_gates(circuit):
    # Get the program from the input circuit
    prog = circuit
    
    # Create a new empty program
    new_prog = QProg()
    
    # Extract instructions from the original program
    origin_circuits = prog.get_circuits()
    origin_gates = prog.get_gates()
    
    # Process each gate in the original program
    for gate in origin_gates:
        # Check if the gate has parameters
        gate_name = gate.get_gate_type()
        
        # For parameterized gates, check if they have been assigned values
        # In pyQPanda, we need to handle parameterized gates differently
        try:
            # Attempt to get the parameter - if it's unassigned, it will cause issues
            param_value = None
            if hasattr(gate, 'get_parameter'):
                param_value = gate.get_parameter()
            
            # If no exception occurs and parameter exists, add the gate
            if param_value is not None:
                new_prog.insert(gate)
        except:
            # If there's an issue getting the parameter, skip this gate
            continue
            
    # Also process sub-circuits if any
    for circ in origin_circuits:
        # Recursively process circuits
        processed_sub_circuit = remove_unassigned_parameterized_gates(circ)
        # Add to new program if it's not empty
        if len(processed_sub_circuit) > 0:
            new_prog.insert(processed_sub_circuit)
    
    return new_prog

# Manual cleanup
machine.finalize()
