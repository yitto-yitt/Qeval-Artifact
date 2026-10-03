# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import QProg, QGate, QMeasure, QCircuit
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def remove_unassigned_parameterized_gates(circuit):
    # Extract the program from the input circuit
    prog = circuit
    
    # Create a new empty program
    new_prog = QProg()
    
    # Get the instructions in the original program
    instructions = prog.get_instructions()
    
    for inst in instructions:
        # Check if the gate has unassigned parameters
        # For pyQPanda, we need to check if it's a parameterized gate
        # and whether the parameter is assigned
        
        # If it's not a parameterized gate, add it to the new program
        if not hasattr(inst, 'get_param'):
            new_prog.insert(inst)
        else:
            # Check if it's a parameterized gate with unassigned parameters
            try:
                param = inst.get_param()
                # If the parameter is not a concrete value (still symbolic), skip it
                if isinstance(param, (int, float)):
                    new_prog.insert(inst)
            except:
                # If getting parameter fails, it might not be parameterized, so include it
                new_prog.insert(inst)
    
    return new_prog

machine.finalize()
