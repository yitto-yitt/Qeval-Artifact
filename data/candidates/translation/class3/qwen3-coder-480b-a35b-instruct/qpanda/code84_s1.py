# EVAL_META: task_id=84, framework=qpanda, class=3
from pyqpanda import *

def controlled_custom_unitary_circuit():
    machine = init(QMachineType.CPU)
    prog = QProg()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    # Define the custom unitary gate with parameters theta=0.3, phi=0.2, lambda=0.1
    custom_gate = U3(0.3, 0.2, 0.1)
    
    # Create controlled version of the custom gate
    controlled_custom_gate = custom_gate.control(qubits[0])
    
    # Apply the controlled gate
    prog.insert(controlled_custom_gate)
    
    return prog
