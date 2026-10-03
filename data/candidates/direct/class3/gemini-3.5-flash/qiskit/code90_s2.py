# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_custom_controlled():
    # Create custom 2-qubit gate
    sub_circ = QuantumCircuit(2, name='custom_gate')
    sub_circ.x(0)
    sub_circ.h(1)
    custom_gate = sub_circ.to_gate()
    
    # Control the gate with 2 control qubits
    controlled_gate = custom_gate.control(2)
    
    # Create 4-qubit circuit
    qc = QuantumCircuit(4)
    # Apply controlled gate: controls are 0 and 3, targets are 1 and 2
    qc.append(controlled_gate, [0, 3, 1, 2])
    
    return qc
