# EVAL_META: task_id=119, framework=cirq, class=3
import cirq
from typing import Union

def create_ripple_carry_adder_circuit(num_state_qubits: int, kind: str):
    # Calculate total number of qubits needed for the ripple carry adder
    # For CDKM adder: 2 * num_state_qubits + 1 (for carry) + 1 (for ancilla)
    total_qubits = 2 * num_state_qubits + 2
    
    # Create qubits
    qubits = [cirq.LineQubit(i) for i in range(total_qubits)]
    
    # Split qubits into groups: A (input1), B (input2), carry_in, ancilla
    a_qubits = qubits[:num_state_qubits]
    b_qubits = qubits[num_state_qubits:2*num_state_qubits]
    carry_qubit = qubits[2*num_state_qubits]
    ancilla_qubit = qubits[2*num_state_qubits+1]
    
    circuit = cirq.Circuit()
    
    # Implement ripple carry adder based on the kind
    if kind == 'full':
        # Full adder implementation
        for i in range(num_state_qubits):
            # Add full adder for each bit position
            circuit.append(full_adder(a_qubits[i], b_qubits[i], 
                                    carry_qubit if i == 0 else ancilla_qubit, 
                                    b_qubits[i], 
                                    ancilla_qubit if i < num_state_qubits - 1 else carry_qubit))
    elif kind == 'half':
        # Half adder implementation for the least significant bit
        circuit.append(half_adder(a_qubits[0], b_qubits[0], b_qubits[0], carry_qubit))
        # Continue with full adders for remaining bits
        for i in range(1, num_state_qubits):
            circuit.append(full_adder(a_qubits[i], b_qubits[i], 
                                    carry_qubit if i == 1 else ancilla_qubit, 
                                    b_qubits[i], 
                                    ancilla_qubit if i < num_state_qubits - 1 else carry_qubit))
    elif kind == 'fixed':
        # Fixed adder - just basic addition without carry propagation optimization
        for i in range(num_state_qubits):
            circuit.append(cirq.CX(a_qubits[i], b_qubits[i]))
    
    return circuit

def half_adder(input_a: cirq.Qid, input_b: cirq.Qid, sum_out: cirq.Qid, carry_out: cirq.Qid):
    """Implement a half adder using CNOT and Toffoli gates"""
    yield cirq.CX(input_a, input_b)
    yield cirq.CX(input_a, sum_out)
    yield cirq.CCX(input_a, input_b, carry_out)

def full_adder(input_a: cirq.Qid, input_b: cirq.Qid, carry_in: cirq.Qid, 
               sum_out: cirq.Qid, carry_out: cirq.Qid):
    """Implement a full adder using CNOT and Toffoli gates"""
    yield cirq.CX(input_a, input_b)
    yield cirq.CX(carry_in, input_b)
    yield cirq.CX(input_a, sum_out)
    yield cirq.CCX(input_a, input_b, carry_out)
    yield cirq.CX(carry_in, input_b)
    yield cirq.CCX(carry_in, input_b, carry_out)
