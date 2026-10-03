# EVAL_META: task_id=69, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import SGate

def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    qc = QuantumCircuit(2)
    
    # Apply H gate on quantum register 0
    qc.h(0)
    
    # Apply Controlled-S gate on quantum registers 0 and 1 (control on 0, target on 1)
    qc.append(SGate(), [1]).control(1, ctrl_state='1').add_bits([qc.qubits[0]], [qc.qubits[1]])
    # Actually implementing CS gate properly
    qc.cry(1.5708, 0, 1)  # This is not correct for S gate
    
    # Let me fix this to properly implement CS gate
    qc = QuantumCircuit(2)
    qc.h(0)
    # Controlled-S gate: if control (qubit 0) is 1, apply S gate to target (qubit 1)
    qc.cp(1.5708, 0, 1)  # cp is controlled-phase, S gate is pi/2 phase
    # Or we can use the proper CS implementation using CNOTs and single-qubit gates
    # Actually S gate is implemented as Rz(pi/2), so CS would be a controlled version
    
    # Better approach: build CS gate explicitly
    qc = QuantumCircuit(2)
    qc.h(0)
    # Implementing CS gate using CNOT and T gates (T^2 = S)
    qc.cp(1.5708, 0, 1)  # This is the same as controlled-S gate
    
    # Apply H gate on quantum register 1
    qc.h(1)
    
    # Apply Controlled-S dagger gate on quantum registers 1 and 0 (control on 1, target on 0)
    # S-dagger has phase -pi/2
    qc.cp(-1.5708, 1, 0)
    
    return qc
