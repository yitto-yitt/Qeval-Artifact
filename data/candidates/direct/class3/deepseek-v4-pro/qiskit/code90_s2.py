# EVAL_META: task_id=90, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_custom_controlled():
    # Create the custom 2-qubit gate: X on qubit 0, H on qubit 1
    custom_qc = QuantumCircuit(2)
    custom_qc.x(0)
    custom_qc.h(1)
    custom_gate = custom_qc.to_gate()
    
    # Add two control qubits to the custom gate
    controlled_gate = custom_gate.control(2)
    
    # Apply to a 4-qubit circuit: controls are 0 and 3, targets are 1 and 2
    qc = QuantumCircuit(4)
    qc.append(controlled_gate, [0, 3, 1, 2])
    
    return qc
