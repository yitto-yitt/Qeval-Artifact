# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    """
    Creates a Cirq circuit implementing a CDKM ripple-carry adder.
    
    Args:
        num_state_qubits: The number of state qubits (size of each operand).
        kind: The kind of adder: 'full', 'half', or 'fixed'.
    
    Returns:
        A cirq.Circuit implementing the CDKM ripple-carry adder.
    """
    # Total number of qubits: 2*num_state_qubits data + 1 carry-in + (num_state_qubits - 1) carries
    # For 'half' kind, the last carry-out is omitted.
    if kind == 'full':
        num_carry_qubits = 1 + (num_state_qubits - 1)
    elif kind == 'half':
        num_carry_qubits = 1 + (num_state_qubits - 2)
    elif kind == 'fixed':
        num_carry_qubits = 1 + (num_state_qubits - 1)
    else:
        raise ValueError(f"Invalid kind: {kind}")
    
    num_qubits = 2 * num_state_qubits + num_carry_qubits
    qubits = cirq.LineQubit.range(num_qubits)
    
    # CDKM ripple carry adder decomposition
    # Based on Cuccaro, Draper, Kutin, Moulton (2004) "A new quantum ripple-carry addition circuit"
    # with reduced ancilla count.
    
    a = qubits[:num_state_qubits]      # First operand
    b = qubits[num_state_qubits:2*num_state_qubits]  # Second operand
    c = qubits[2*num_state_qubits:]    # Carry qubits
    
    circuit = cirq.Circuit()
    
    # MAJ (Majority) and UMA (UnMajority and Add) gates defined as subroutines
    def maj(cx, cy, cz):
        """MAJ gate: computes majority of three qubits."""
        return [
            cirq.CNOT(cz, cy),
            cirq.CNOT(cz, cx),
            cirq.CCNOT(cx, cy, cz)
        ]
    
    def uma(cx, cy, cz):
        """UMA gate: uncomputes majority and computes sum."""
        return [
            cirq.CCNOT(cx, cy, cz),
            cirq.CNOT(cz, cx),
            cirq.CNOT(cx, cy)
        ]
    
    # Step 1: Initial carry-in processing
    circuit.append(maj(c[0], b[0], a[0]))
    
    # Step 2: Chain of MAJ gates for bits 1 to n-1
    for i in range(1, num_state_qubits):
        circuit.append(maj(a[i-1], b[i], a[i]))
    
    # Step 3: If 'full' or 'fixed', compute final carry-out with CNOT
    if kind in ('full', 'fixed'):
        if num_state_qubits > 1:
            circuit.append(cirq.CNOT(a[num_state_qubits-1], b[num_state_qubits-1]))
    
    # Step 4: Reverse chain of UMA gates
    for i in reversed(range(1, num_state_qubits)):
        circuit.append(uma(a[i-1], b[i], a[i]))
    
    # Step 5: Final UMA for bit 0
    circuit.append(uma(c[0], b[0], a[0]))
    
    return circuit
