# EVAL_META: task_id=119, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    # Calculate total number of qubits needed
    if kind == 'full':
        total_qubits = 2 * num_state_qubits + 1
    elif kind == 'half':
        total_qubits = 2 * num_state_qubits
    elif kind == 'fixed':
        total_qubits = 2 * num_state_qubits + 1
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    
    # Create the quantum program and machine
    prog = QProg()
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(total_qubits)
    
    # For ripple carry adder implementation, we need to manually construct the circuit
    # This is based on the structure of CDKM adder
    
    # Define helper functions for full adder
    def full_adder(prog, a, b, c_in, sum_out, c_out):
        # First part of full adder
        prog << CNOT(b, sum_out) << CNOT(a, sum_out)
        prog << CCNOT(a, b, c_out)
        
        # Second part
        prog << CNOT(c_in, sum_out) << CCNOT(c_in, sum_out, c_out)
        
        # Third part
        prog << CNOT(a, b) << CCNOT(b, sum_out, c_out)
        prog << CNOT(a, b)
    
    # Build ripple carry adder based on kind
    if kind == 'full':
        # Full adder has input_a[0:num_state_qubits], input_b[0:num_state_qubits], carry_in, 
        # and outputs sum[0:num_state_qubits] and final carry out
        
        # Initialize carry bit (last qubit is carry out, second last is carry in)
        carry_in = q[2 * num_state_qubits]
        carry_out = q[2 * num_state_qubits + 1]
        
        # Process each bit position
        for i in range(num_state_qubits):
            a_bit = q[i]
            b_bit = q[num_state_qubits + i]
            
            if i == 0:
                # For first bit, use carry_in as the carry input
                sum_bit = q[2 * num_state_qubits]  # temporary storage location
                # We'll need to remap this properly
                # Actually, let's set up proper bit positions
                temp_sum = qvm.qAlloc_many(num_state_qubits)  # temporary for sum bits
                
                # For first bit: inputs are a[0], b[0], carry_in -> sum[0], new_carry
                prog << CNOT(b_bit, temp_sum[i]) << CNOT(a_bit, temp_sum[i])
                prog << CCNOT(a_bit, b_bit, q[2*num_state_qubits])  # intermediate carry
                
                # Connect with carry_in
                prog << CNOT(carry_in, temp_sum[i])
                prog << CCNOT(carry_in, temp_sum[i], q[2*num_state_qubits])
                
                # Now temp_sum[i] holds the sum, but we want it in the right place
                # Copy temp_sum[i] to actual sum position
                prog << CNOT(temp_sum[i], q[i])  # copy to original a position
            else:
                # Subsequent bits: use previous carry as input
                prev_carry = q[2*num_state_qubits]  # using one of our extra qubits
                # We need to implement the logic properly
                
                # Reset temp sum bit if needed
                # Calculate new sum and carry
                prog << CNOT(b_bit, q[i]) << CNOT(q[i-1], q[i])  # sum calculation
                prog << CCNOT(q[i-1], b_bit, q[2*num_state_qubits])  # carry calc
                
                # Incorporate carry from previous stage
                prog << CNOT(q[2*num_state_qubits - 1] if i > 1 else carry_in, q[i])
                prog << CCNOT(q[2*num_state_qubits - 1] if i > 1 else carry_in, q[i], q[2*num_state_qubits])
    
    elif kind == 'half':
        # Half adder adds two numbers without initial carry
        for i in range(num_state_qubits):
            a_bit = q[i]
            b_bit = q[num_state_qubits + i]
            
            # XOR operation for sum
            prog << CNOT(b_bit, a_bit)
            
            # AND operation for carry (if there's space)
            if i < num_state_qubits - 1:  # Store carry in next a position temporarily
                if i+1 < num_state_qubits:
                    prog << CCNOT(q[i], q[num_state_qubits + i], q[i+1])
    
    elif kind == 'fixed':
        # Similar to full but may have different carry handling
        carry_qubit = q[2 * num_state_qubits]
        for i in range(num_state_qubits):
            a_bit = q[i]
            b_bit = q[num_state_qubits + i]
            
            # Sum calculation
            prog << CNOT(b_bit, a_bit)
            
            # Carry propagation
            if i == 0:
                prog << CCNOT(a_bit, b_bit, carry_qubit)
            else:
                prog << CNOT(q[2*num_state_qubits - 1], a_bit)  # incorporate previous carry
                prog << CCNOT(q[2*num_state_qubits - 1], a_bit, carry_qubit)
    
    # Return the program
    return prog
