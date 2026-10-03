# EVAL_META: task_id=119, framework=cirq, class=3
import cirq
from cirq.contrib.quirk import QuirkOp

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    # Calculate total number of qubits needed for ripple carry adder
    # For CDKM adder: 2 * num_state_qubits + 1 (for carry) + 1 (for ancilla)
    total_qubits = 2 * num_state_qubits + 2
    
    # Create qubits
    qubits = [cirq.LineQubit(i) for i in range(total_qubits)]
    
    # Split qubits into groups: A (input1), B (input2), carry_in, ancillas
    a_qubits = qubits[:num_state_qubits]
    b_qubits = qubits[num_state_qubits:2*num_state_qubits]
    carry_qubit = qubits[2*num_state_qubits]
    ancilla_qubit = qubits[2*num_state_qubits+1] if total_qubits > 2*num_state_qubits+1 else None
    
    circuit = cirq.Circuit()
    
    # Implement ripple carry adder based on kind
    if kind == 'full':
        # Full adder implementation
        for i in range(num_state_qubits):
            # Add controlled operations for ripple carry logic
            if i == 0:
                # Half adder for first bit
                circuit.append(cirq.CX(a_qubits[i], b_qubits[i]))
                circuit.append(cirq.CCX(a_qubits[i], b_qubits[i], carry_qubit))
            else:
                # Full adder for subsequent bits
                circuit.append(cirq.CX(a_qubits[i], b_qubits[i]))
                circuit.append(cirq.CCX(a_qubits[i], b_qubits[i], ancilla_qubit))
                circuit.append(cirq.CX(carry_qubit, b_qubits[i]))
                circuit.append(cirq.CCX(carry_qubit, ancilla_qubit, b_qubits[i]))
                circuit.append(cirq.CX(ancilla_qubit, carry_qubit))
                circuit.append(cirq.CNOT(ancilla_qubit, b_qubits[i]))
    elif kind == 'half':
        # Half adder implementation - simpler version
        for i in range(num_state_qubits):
            circuit.append(cirq.CX(a_qubits[i], b_qubits[i]))
    elif kind == 'fixed':
        # Fixed adder - just basic addition without carry propagation
        for i in range(num_state_qubits):
            circuit.append(cirq.CX(a_qubits[i], b_qubits[i]))
    
    return circuit
