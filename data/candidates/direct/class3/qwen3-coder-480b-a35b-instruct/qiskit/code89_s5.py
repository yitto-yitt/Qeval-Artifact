# EVAL_META: task_id=89, framework=qiskit, class=3
from qiskit import QuantumCircuit

def create_controlled_hgate():
    qc = QuantumCircuit(3)
    qc.ch(0, 2)  # Controlled-Hadamard with qubit 0 as control and qubit 2 as target
    qc.ch(1, 2)  # Controlled-Hadamard with qubit 1 as control and qubit 2 as target
    # To make it a true 2-controlled H gate, we need to use ancilla or decompose differently
    # Using the standard approach with Toffoli and H gates
    qc = QuantumCircuit(3)
    # Implement CCX (Toffoli) then H on target, then CCX again
    # However, Qiskit doesn't have direct CH with multiple controls
    # We'll implement using the decomposition
    
    # Reset circuit
    qc = QuantumCircuit(3)
    
    # Create a temporary circuit for the controlled-H
    # We can implement a doubly-controlled H gate by using the fact that H = RY(pi/2) up to phase
    # But the most straightforward way is to use the built-in method if available
    # Since we need two controls, we'll decompose manually
    
    # Use a Toffoli gate followed by H on target when both controls are 1
    # Actually, let's use the proper decomposition for a controlled-H gate with 2 controls
    qc.ccx(0, 1, 2)  # This would be wrong - this applies X when both controls are 1
    # Need to reset and do correct implementation
    
    qc = QuantumCircuit(3)
    # Proper implementation of doubly controlled Hadamard gate
    # We'll use the decomposition where we apply H to target only when both controls are |1>
    
    # Apply controlled rotations to implement controlled-H
    # First, we note that H = RZ(π)RY(π/2)RZ(-π) up to global phase
    # Or more directly, we can use the fact that controlled-H can be built from other gates
    
    # A proper doubly-controlled H gate can be implemented as follows:
    # Use the decomposition based on the fact that any multi-controlled gate can be decomposed
    qc = QuantumCircuit(3)
    
    # For a 2-controlled H gate, we can use the following approach:
    # Implement the controlled version of H gate using the general method
    # H gate is self-inverse, so we can use specific decomposition
    
    # One way is to use the decomposition involving CNOTs and single-qubit gates
    qc.h(2)  # Start with H on target
    qc.t(2)  # T gate 
    qc.cx(1, 2)  # CNOT with qubit 1 as control and qubit 2 as target
    qc.tdg(2)  # T-dagger
    qc.cx(1, 2)  # CNOT again
    qc.t(2)  # T
    qc.cx(0, 2)  # CNOT with qubit 0 as control and qubit 2 as target
    qc.tdg(2)  # T-dagger
    qc.cx(1, 2)  # CNOT
    qc.t(2)  # T
    qc.cx(0, 2)  # CNOT
    qc.tdg(2)  # T-dagger
    qc.cx(1, 2)  # CNOT
    qc.t(2)  # T
    qc.cx(0, 2)  # CNOT
    qc.tdg(2)  # T-dagger
    qc.cx(1, 2)  # CNOT
    qc.tdg(2)  # T-dagger
    qc.h(2)  # Final H gate
    
    # Actually, this is getting complex. Let me use the proper method with built-in functionality
    qc = QuantumCircuit(3)
    # Use the quantum register and append a multi-controlled H gate
    # In Qiskit, we can build this with the general control mechanism
    
    # The simplest way is to use the control method of the H gate
    h_gate = qc.h(2).to_instruction()  # Get H gate
    # Then create a controlled version with 2 controls
    controlled_h = h_gate.control(2)
    
    # Reset and rebuild properly
    qc = QuantumCircuit(3)
    # Create a Hadamard gate
    from qiskit.circuit.library import HGate
    h_gate = HGate()
    # Make it doubly controlled
    controlled_h = h_gate.control(2)
    # Append to circuit with qubits 0,1 as controls and 2 as target
    qc.append(controlled_h, [0, 1, 2])
    
    return qc
