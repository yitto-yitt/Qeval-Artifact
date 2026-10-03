# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_custom_controlled():
    # Create a 2-qubit gate with X on qubit 0 and H on qubit 1
    sub_circ = QuantumCircuit(2, name='custom_gate')
    sub_circ.x(0)
    sub_circ.h(1)
    custom_gate = sub_circ.to_gate()
    
    # Add two control qubits
    controlled_gate = custom_gate.control(2)
    
    # Create a 4-qubit circuit
    qc = QuantumCircuit(4)
    
    # Apply controlled gate with controls [0, 3] and targets [1, 2]
    qc.append(controlled_gate, [0, 3, 1, 2])
    
    return qc
