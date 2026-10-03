# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_custom_controlled():
    # Create a custom 2-qubit gate
    sub_circ = QuantumCircuit(2, name='custom')
    sub_circ.x(0)
    sub_circ.h(1)
    custom_gate = sub_circ.to_gate()
    
    # Add two control qubits to the gate
    controlled_gate = custom_gate.control(2)
    
    # Create a 4-qubit circuit and apply the controlled gate
    qc = QuantumCircuit(4)
    # Qubits 0 and 3 as controls, qubits 1 and 2 as targets
    qc.append(controlled_gate, [0, 3, 1, 2])
    
    return qc
