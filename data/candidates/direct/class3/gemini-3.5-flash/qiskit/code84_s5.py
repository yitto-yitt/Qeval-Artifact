# EVAL_META: task_id=84, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import UGate

def controlled_custom_unitary_circuit():
    # Create a 2-qubit quantum circuit
    qc = QuantumCircuit(2)
    
    # Define a custom 1-qubit unitary gate with angles 0.3, 0.2, and 0.1
    u_gate = UGate(0.3, 0.2, 0.1)
    
    # Convert it to a controlled gate
    cu_gate = u_gate.control(num_ctrl_qubits=1)
    
    # Apply it with qubit 0 as control and qubit 1 as target
    qc.append(cu_gate, [0, 1])
    
    return qc
