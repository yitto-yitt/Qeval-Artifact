# EVAL_META: task_id=90, framework=qpanda, class=3
from pyqpanda import *

def create_custom_controlled():
    # Create the custom 2-qubit gate with X on qubit 0 and H on qubit 1
    qc1 = QProg()
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits1 = qvm.qAlloc_many(2)
    cbits1 = qvm.cAlloc_many(2)
    
    # Build the custom gate circuit
    qc1.insert(X(qubits1[0]))
    qc1.insert(H(qubits1[1]))
    
    # Convert to a custom gate
    custom_gate = qc1.gate()
    
    # Create the main 4-qubit circuit
    qc2 = QProg()
    qvm2 = CPUQVM()
    qvm2.init_qvm()
    qubits2 = qvm2.qAlloc_many(4)
    cbits2 = qvm2.cAlloc_many(4)
    
    # Apply the controlled version of the custom gate
    # Using qubits 0 and 3 as controls, and qubits 1 and 2 as targets
    controlled_gate = custom_gate.control([qubits2[0], qubits2[3]])
    qc2.insert(controlled_gate)
    
    return qc2
