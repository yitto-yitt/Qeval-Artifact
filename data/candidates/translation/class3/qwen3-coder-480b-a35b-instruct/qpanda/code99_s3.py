# EVAL_META: task_id=99, framework=qpanda, class=3
from pyqpanda3.core import *
from pyqpanda3 import *

def remove_unassigned_parameterized_gates(circuit):
    # Create a new quantum program without unassigned parameterized gates
    new_prog = QProg()
    qvm = getQVM(1)
    qvm.initQVM()
    
    # Get qubit count from original circuit
    qvec = qvm.qAlloc_many(circuit.get_max_qubit_num() + 1)
    
    # Iterate through the original circuit's gates
    for gate in circuit.getGates():
        # Check if the gate has unassigned parameters
        # In pyQPanda3, parameterized gates have parameters that need to be checked
        is_param_gate = False
        
        # For rotation gates like RX, RY, RZ, U3 etc., check if they have symbolic parameters
        if hasattr(gate, 'get_parameter'):
            param = gate.get_parameter()
            # If parameter is symbolic (not a fixed value), it's unassigned
            if isinstance(param, str) or (hasattr(param, '__class__') and 'Parameter' in str(type(param))):
                is_param_gate = True
                
        # If it's not a parameterized gate or it has assigned parameters, add it
        if not is_param_gate:
            new_prog.insert(gate)
    
    qvm.finalize()
    return new_prog
