# EVAL_META: task_id=119, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    # Calculate total number of qubits needed for ripple carry adder
    # For pyQPanda, we need to manually construct the adder circuit
    qubits = machine.qAlloc_many(2 * num_state_qubits + 1)  # Two registers + carry
    
    # Create empty circuit
    prog = pq.QProg()
    
    # Implement ripple carry adder manually based on the kind
    if kind == 'full':
        # Full adder implementation - includes input carry handling
        for i in range(num_state_qubits):
            if i == 0:
                # First bit: half adder
                prog.insert(pq.CNOT(qubits[i], qubits[num_state_qubits + i]))
                prog.insert(pq.TOFFOLI(qubits[i], qubits[num_state_qubits + i], qubits[2*num_state_qubits]))
            else:
                # Subsequent bits: full adder
                # Add carry from previous stage
                prog.insert(pq.CNOT(qubits[i-1], qubits[2*num_state_qubits]))
                prog.insert(pq.CNOT(qubits[num_state_qubits+i-1], qubits[2*num_state_qubits]))
                
                # Sum calculation
                prog.insert(pq.CNOT(qubits[i], qubits[num_state_qubits + i]))
                prog.insert(pq.TOFFOLI(qubits[i], qubits[num_state_qubits + i], qubits[2*num_state_qubits]))
    elif kind == 'half':
        # Half adder implementation - no initial carry
        for i in range(num_state_qubits):
            prog.insert(pq.CNOT(qubits[i], qubits[num_state_qubits + i]))
            if i < num_state_qubits - 1:  # Only connect carry for non-last qubit
                prog.insert(pq.TOFFOLI(qubits[i], qubits[num_state_qubits + i], qubits[2*num_state_qubits]))
    elif kind == 'fixed':
        # Fixed adder - similar to full but might have different carry behavior
        for i in range(num_state_qubits):
            prog.insert(pq.CNOT(qubits[i], qubits[num_state_qubits + i]))
            if i < num_state_qubits - 1:
                prog.insert(pq.TOFFOLI(qubits[i], qubits[num_state_qubits + i], qubits[2*num_state_qubits]))
    
    return prog

# Manual cleanup
machine.finalize()
