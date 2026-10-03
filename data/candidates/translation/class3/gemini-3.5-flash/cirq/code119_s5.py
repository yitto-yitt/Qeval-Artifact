# EVAL_META: task_id=119, framework=cirq, class=3
import cirq
from cirq.contrib.quirk import QuirkOp

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    # Calculate total number of qubits needed for ripple carry adder
    # For CDKM adder: 2 * num_state_qubits + 1 (for carry) + 1 (for ancilla)
    total_qubits = 2 * num_state_qubits + 2
    
    # Create qubits
    qubits = cirq.LineQubit.range(total_qubits)
    
    # Split qubits into groups: A (input1), B (input2), carry_in, ancillas
    a_qubits = qubits[:num_state_qubits]
    b_qubits = qubits[num_state_qubits:2*num_state_qubits]
    carry_qubit = qubits[2*num_state_qubits]
    ancilla_qubit = qubits[2*num_state_qubits+1] if total_qubits > 2*num_state_qubits+1 else None
    
    circuit = cirq.Circuit()
    
    # Implement ripple carry adder manually based on CDKM algorithm
    # This is a simplified version that mimics the behavior of CDKMRippleCarryAdder
    for i in range(num_state_qubits):
        # Full adder for each bit position
        if i == 0:
            # First bit: use input carry
            circuit.append(cirq.CCX(a_qubits[i], b_qubits[i], carry_qubit))
            circuit.append(cirq.CX(a_qubits[i], b_qubits[i]))
            circuit.append(cirq.CCX(a_qubits[i], carry_qubit, b_qubits[i]))
        else:
            # Subsequent bits: use previous sum as input
            prev_carry = ancilla_qubit if ancilla_qubit is not None else qubits[2*num_state_qubits + i - 1]
            next_carry = qubits[2*num_state_qubits + i] if i < num_state_qubits - 1 or ancilla_qubit is None else ancilla_qubit
            
            circuit.append(cirq.CCX(a_qubits[i], b_qubits[i], next_carry))
            circuit.append(cirq.CX(a_qubits[i], b_qubits[i]))
            circuit.append(cirq.CCX(prev_carry, b_qubits[i], next_carry))
    
    return circuit