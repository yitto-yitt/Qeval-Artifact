# EVAL_META: task_id=118, framework=pennylane, class=3
import pennylane as qml

def create_c3sx_circuit():
    dev = qml.device('default.qubit', wires=4)
    
    @qml.qnode(dev)
    def circuit():
        # Implementing C3SX (controlled-controlled-controlled-X) gate manually
        # This is equivalent to having three control qubits and one target qubit
        # The X gate is applied to the target only when all three controls are |1>
        
        # Using Toffoli gates and additional ancilla to decompose C3X
        # First create a Toffoli gate on qubits 0,1,2 with ancilla at 4
        qml.Toffoli(wires=[0, 1, 2])
        # Then use that result with qubit 2 as control and qubit 3 as target
        # We need to temporarily move the result to an ancilla and back
        
        # A proper decomposition for C3X requires multiple Toffoli gates
        # For a C3X gate: if qubits 0,1,2 are control and 3 is target
        # We'll implement it using Toffoli gates with ancillas
        
        # Reset the temporary wire usage - we'll implement C3SX directly
        # C3SX can be decomposed as C3X followed by S-dagger
        # But since PennyLane doesn't have direct C3X, we'll build it
        
        # Decomposition of C3X using Toffoli gates (requires ancilla)
        # For 4-qubit system without extra ancilla, we need to be more creative
        # Actually, let's just implement the equivalent operation using basic controlled operations
        
        # In PennyLane, we can build this using ControlledQubitUnitary or series of Toffoli
        # Since C3SX = C3X with S† on target when controls satisfied
        # Let's implement as a controlled operation where X is applied to qubit 3 if qubits 0,1,2 are all 1
        
        # We'll implement the C3X gate using multiple Toffoli gates
        # This requires ancillary qubits, but since we only have 4 qubits total,
        # we'll have to implement this differently or assume a higher-level construction
        
        # Actually, we should use qml.ctrl to apply X when 3 control qubits are active
        qml.ctrl(qml.PauliX, control=[0, 1, 2])(wires=3)
        
        return qml.state()
    
    # Return the tape containing the operations
    circuit()
    return circuit.tape
