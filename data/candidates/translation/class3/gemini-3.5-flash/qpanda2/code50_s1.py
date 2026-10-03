# EVAL_META: task_id=50, framework=qpanda2, class=3
from pyqpanda import *

# Initialize CPUQVM and qAlloc_many at global scope
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(16)

def remove_gate_in_position(circuit, position):
    nodes = []
    for node in circuit:
        nodes.append(node)
    
    nodes.pop(position)
    
    if isinstance(circuit, QCircuit):
        new_circuit = QCircuit()
    else:
        new_circuit = QProg()
        
    for node in nodes:
        new_circuit.insert(node)
        
    return new_circuit

# Manual Cleanup
machine.finalize()
