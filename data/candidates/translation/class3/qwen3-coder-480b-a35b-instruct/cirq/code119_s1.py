# EVAL_META: task_id=119, framework=cirq, class=3
import cirq
from cirq import ops
import numpy as np

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    # Create the qubit registers
    # For CDKM ripple carry adder, we need:
    # - num_state_qubits for first operand
    # - num_state_qubits for second operand  
    # - 1 carry qubit
    # - 1 zero qubit
    total_qubits = 2 * num_state_qubits + 2
    qubits = [cirq.LineQubit(i) for i in range(total_qubits)]
    
    # Split qubits into registers
    a_qubits = qubits[:num_state_qubits]
    b_qubits = qubits[num_state_qubits:2*num_state_qubits]
    carry_qubit = qubits[2*num_state_qubits]
    zero_qubit = qubits[2*num_state_qubits + 1]
    
    circuit = cirq.Circuit()
    
    # Implement CDKM ripple carry adder based on the kind
    if kind == 'half':
        # Half adder - no initial carry
        # Start with the least significant bit
        circuit.append(cirq.X(carry_qubit))  # Initialize carry to |1>
        
        for i in range(num_state_qubits):
            # Apply the MAJ gate sequence
            if i == 0:
                # For half adder, first step is different
                circuit.append(cirq.TOFFOLI(a_qubits[i], carry_qubit, zero_qubit))
                circuit.append(cirq.CNOT(a_qubits[i], carry_qubit))
                circuit.append(cirq.TOFFOLI(b_qubits[i], carry_qubit, zero_qubit))
                circuit.append(cirq.CNOT(b_qubits[i], carry_qubit))
                circuit.append(cirq.TOFFOLI(zero_qubit, carry_qubit, b_qubits[i]))
                circuit.append(cirq.CNOT(b_qubits[i], carry_qubit))
                circuit.append(cirq.CNOT(a_qubits[i], b_qubits[i]))
            else:
                # Full adder steps for remaining bits
                circuit.append(cirq.TOFFOLI(a_qubits[i], b_qubits[i], zero_qubit))
                circuit.append(cirq.CNOT(a_qubits[i], b_qubits[i]))
                circuit.append(cirq.TOFFOLI(carry_qubit, b_qubits[i], zero_qubit))
                circuit.append(cirq.CNOT(b_qubits[i], carry_qubit))
                circuit.append(cirq.TOFFOLI(zero_qubit, carry_qubit, b_qubits[i]))
                circuit.append(cirq.CNOT(b_qubits[i], carry_qubit))
                
        # Uncompute ancilla
        circuit.append(cirq.CNOT(a_qubits[-1], b_qubits[-1]))
        circuit.append(cirq.TOFFOLI(carry_qubits[-1] if num_state_qubits > 1 else carry_qubit, 
                                  b_qubits[-1], zero_qubit))
        
    elif kind == 'full' or kind == 'fixed':
        # Full adder - with initial carry
        # Initialize carry based on kind
        if kind == 'fixed':
            circuit.append(cirq.X(carry_qubit))  # Set initial carry
            
        # Apply the ripple carry addition logic
        ancilla_qubit = zero_qubit
        
        # Forward pass - compute carries
        for i in range(num_state_qubits):
            # MAJ gate implementation
            if i == 0 and kind != 'fixed':
                # No initial carry for regular full adder on first bit
                circuit.append(cirq.TOFFOLI(a_qubits[i], b_qubits[i], ancilla_qubit))
                circuit.append(cirq.CNOT(a_qubits[i], b_qubits[i]))
                circuit.append(cirq.TOFFOLI(b_qubits[i], carry_qubit, ancilla_qubit))
            else:
                control1 = a_qubits[i]
                control2 = b_qubits[i] if i == 0 else b_qubits[i]
                target = ancilla_qubit
                circuit.append(cirq.TOFFOLI(control1, control2, target))
                circuit.append(cirq.CNOT(control1, control2))
                circuit.append(cirq.TOFFOLI(control2, carry_qubit, target))
            
            circuit.append(cirq.CNOT(control2, carry_qubit))
            
        # Backward pass - uncompute and generate sum
        for i in reversed(range(num_state_qubits)):
            if i == 0 and kind != 'fixed':
                circuit.append(cirq.TOFFOLI(b_qubits[i], carry_qubit, ancilla_qubit))
                circuit.append(cirq.CNOT(b_qubits[i], carry_qubit))
                circuit.append(cirq.TOFFOLI(a_qubits[i], b_qubits[i], ancilla_qubit))
                circuit.append(cirq.CNOT(a_qubits[i], b_qubits[i]))
            else:
                # Standard uncomputation
                circuit.append(cirq.TOFFOLI(carry_qubit, b_qubits[i], ancilla_qubit))
                circuit.append(cirq.CNOT(b_qubits[i], carry_qubit))
                circuit.append(cirq.CNOT(a_qubits[i], b_qubits[i]))
                circuit.append(cirq.TOFFOLI(a_qubits[i], b_qubits[i], ancilla_qubit))
                
    return circuit
