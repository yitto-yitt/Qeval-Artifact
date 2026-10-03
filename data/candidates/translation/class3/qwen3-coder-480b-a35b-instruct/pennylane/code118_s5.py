# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    def circuit():
        # Implementing C3SX gate using Toffoli gates and single-qubit rotations
        # C3SX can be decomposed as follows:
        # Apply Toffoli on qubits 0,1,2 controlled by first two as control, target on 3
        # Then apply S on target (qubit 3)
        # Then apply another Toffoli
        
        # First, we need to implement the C3SX gate manually since PennyLane doesn't have it directly
        # A C3SX gate is a 3-controlled sqrt-X gate
        
        # We'll use a decomposition approach for 3-controlled X then take square root
        # Using ancilla-free decomposition for 3-controlled X gate would require more complex setup
        # For now, implementing using multi-controlled operations available in PennyLane
        
        # Since direct C3SX is not available, we construct it using multiple Toffoli gates
        # and S gate based on standard decomposition
        
        # The C3SX gate is equivalent to applying a controlled version of SX (sqrt(X)) 
        # where the SX is applied to qubit 3 when qubits 0, 1, and 2 are all in |1> state
        
        # In PennyLane, we can use MultiControlledX with custom matrix for the operation
        # But SX is sqrt(X), so we need to implement a 3-controlled sqrt(X) gate
        
        # We'll implement this using a sequence of operations that achieves the same result
        # This is a simplified approach using the fact that SX = RZ(-pi/2)RY(pi/2)RZ(pi/2)
        
        # However, the most straightforward way is to use qml.ctrl with qml.SX
        qml.ctrl(qml.SX, control=[0, 1, 2])(wires=3)
    
    return circuit
