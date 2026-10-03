# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_custom_controlled():
    # Create a custom 2-qubit gate
    custom_circ = QuantumCircuit(2, name='custom_gate')
    custom_circ.x(0)
    custom_circ.h(1)
    custom_gate = custom_circ.to_gate()
    
    # Add two control qubits
    controlled_gate = custom_gate.control(2)
    
    # Create a 4-qubit circuit and apply the controlled gate
    qc = QuantumCircuit(4)
    # Controls: 0 and 3, Targets: 1 and 2
    qc.append(controlled_gate, [0, 3, 1, 2])
    
    return qc
