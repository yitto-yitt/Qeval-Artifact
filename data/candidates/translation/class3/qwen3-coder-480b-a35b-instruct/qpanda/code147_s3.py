# EVAL_META: task_id=147, framework=qpanda, class=3
import pyqpanda3.core as pq

def mcy(qc):
    # Get the qubits from the circuit
    qubits = qc.qubits()
    
    # Create a multi-controlled Y gate using X gate with Ry rotation
    # Y gate can be implemented as RY(pi) followed by S† and S gates, but simpler approach
    # is to use the fact that Y = -i * X * Z, we'll implement multi-controlled Y via decomposition
    
    # For multi-controlled Y, we can use the fact that Y = H * Z * H
    # But in pyQPanda3, we need to implement it using available gates
    # Y gate is equivalent to RY(pi) up to global phase
    
    # Apply multi-controlled RY gate (equivalent to multi-controlled Y)
    # We'll use the decomposition approach for multi-controlled Y
    ctrl_qubits = [qubits[0], qubits[1], qubits[2], qubits[3]]
    target_qubit = qubits[4]
    
    # Using Ry gate with angle pi for Y operation
    qc.mcry(ctrl_qubits, target_qubit, pq.PI)
    
    return qc
