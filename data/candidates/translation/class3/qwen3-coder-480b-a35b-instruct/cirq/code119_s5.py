# EVAL_META: task_id=119, framework=cirq, class=3
import cirq
from typing import Union

def create_ripple_carry_adder_circuit(num_state_qubits: int, kind: str) -> cirq.Circuit:
    # Calculate total number of qubits needed
    if kind == 'full':
        total_qubits = 2 * num_state_qubits + 2  # two registers + carry + ancilla
    elif kind == 'half':
        total_qubits = 2 * num_state_qubits + 1  # two registers + carry
    elif kind == 'fixed':
        total_qubits = 2 * num_state_qubits + 1  # two registers + carry
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    
    # Create qubits
    qubits = [cirq.LineQubit(i) for i in range(total_qubits)]
    
    # Split qubits into appropriate registers
    input_a = qubits[:num_state_qubits]
    input_b = qubits[num_state_qubits:2*num_state_qubits]
    
    circuit = cirq.Circuit()
    
    # Implement ripple carry adder based on kind
    if kind == 'full':
        carry_qubit = qubits[2*num_state_qubits]
        ancilla_qubit = qubits[2*num_state_qubits+1]
        
        # Full adder implementation using Cuccaro et al. approach
        for i in range(num_state_qubits):
            if i == 0:
                # First bit: half adder
                circuit.append([
                    cirq.CX(input_b[i], input_a[i]),
                    cirq.CX(input_a[i], carry_qubit),
                    cirq.CX(input_b[i], input_a[i])
                ])
            else:
                # Subsequent bits: full adder
                circuit.append([
                    cirq.CX(input_a[i-1], carry_qubit),
                    cirq.CX(input_b[i], carry_qubit),
                    cirq.TOFFOLI(input_a[i-1], input_b[i], ancilla_qubit),
                    cirq.CX(input_a[i], ancilla_qubit),
                    cirq.TOFFOLI(input_a[i-1], input_b[i], ancilla_qubit),
                    cirq.CX(input_a[i-1], carry_qubit),
                    cirq.CX(input_b[i], input_a[i]),
                    cirq.CX(input_b[i], carry_qubit),
                    cirq.CX(input_b[i], input_a[i])
                ])
                
    elif kind == 'half':
        carry_qubit = qubits[2*num_state_qubits]
        
        # Half adder implementation
        for i in range(num_state_qubits):
            circuit.append([
                cirq.CX(input_b[i], input_a[i]),
                cirq.CX(input_a[i], carry_qubit),
                cirq.CX(input_b[i], input_a[i])
            ])
            
    elif kind == 'fixed':
        carry_qubit = qubits[2*num_state_qubits]
        
        # Fixed adder implementation similar to half adder but with carry propagation
        for i in range(num_state_qubits):
            if i == 0:
                circuit.append([
                    cirq.CX(input_b[i], input_a[i]),
                    cirq.CX(input_a[i], carry_qubit),
                    cirq.CX(input_b[i], input_a[i])
                ])
            else:
                circuit.append([
                    cirq.CX(input_a[i-1], input_a[i]),
                    cirq.CX(input_b[i], input_a[i]),
                    cirq.CX(input_a[i-1], carry_qubit),
                    cirq.CX(input_b[i], carry_qubit)
                ])
    
    return circuit
