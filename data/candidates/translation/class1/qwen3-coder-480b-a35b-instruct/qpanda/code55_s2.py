# EVAL_META: task_id=55, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(9)  # 3 for a, 3 for b, 3 for ancillary
    cbits = machine.cAlloc_many(3)   # 3 classical bits for measurement
    
    prog = pq.QProg()
    
    # Split qubits
    qr_a = qubits[:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]
    
    # Format inputs to 3-bit binary strings
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    # Initialize input states (flip if bit is 0 to make it 1, then we'll handle the logic properly)
    for i in range(3):
        if a_str[2-i] == '0':
            prog.insert(pq.X(qr_a[i]))
        if b_str[2-i] == '0':
            prog.insert(pq.X(qr_b[i]))
    
    # Apply CCX gates to compute AND of each pair (a_i AND b_i -> ancillary_i)
    for i in range(3):
        prog.insert(pq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
    
    # To get OR, we use De Morgan's law: A OR B = NOT(NOT A AND NOT B)
    # But since we want (a_i OR b_i), let's think differently:
    # Actually, we want to compute NOT((NOT a_i) AND (NOT b_i))
    # So first we need to revert the initial flipping if any...
    
    # Actually, let's reconsider the approach:
    # We want a | b, so we should prepare the qubits such that they represent the actual values
    # If a bit is 1, we leave it as is. If it's 0, we don't flip it initially.
    # Then compute NOT of AND of NOTs to get OR.
    
    # Reinitialize the program
    prog = pq.QProg()
    
    # Set up initial states correctly
    for i in range(3):
        if a & (1 << i):  # Check if the i-th bit (in normal order) is set
            pass  # Already in |0>, need to flip to |1>
            prog.insert(pq.X(qr_a[2-i]))  # Map to reverse index
        if b & (1 << i):
            pass  # Already in |0>, need to flip to |1>
            prog.insert(pq.X(qr_b[2-i]))  # Map to reverse index
    
    # Actually, let me follow the original Qiskit logic more carefully
    prog = pq.QProg()
    
    a_str = format(a, '03b')  # e.g., if a=5, a_str='101'
    b_str = format(b, '03b')  # e.g., if b=3, b_str='011'
    
    # In Qiskit, a[2-i] means we're accessing the bits in reverse order to match qubit indexing
    for i in range(3):
        if a_str[2-i] == '1':  # If the bit should be 1, flip it from default 0
            prog.insert(pq.X(qr_a[i]))
        if b_str[2-i] == '1':
            prog.insert(pq.X(qr_b[i]))
    
    # Compute AND of a_i and b_i for each position in ancilla
    for i in range(3):
        prog.insert(pq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
    
    # Now we have (a_0 & b_0), (a_1 & b_1), (a_2 & b_2) in ancillary
    # For OR: we want a|b, which means at least one of a or b is 1
    # But this ancillary contains a&b. 
    # Actually, let's just follow the Qiskit code exactly:
    # The Qiskit code computes a&b in ancillary, then applies X to all ancilla, then measures.
    # This gives us the complement of the AND.
    # Wait, that doesn't seem right for OR.
    
    # Let me re-read: Qiskit code does ccx (AND) then X on ancilla then measure.
    # That would give NOT(AND) = NAND.
    # That doesn't seem like OR.
    
    # Looking again at the Qiskit code:
    # It flips the inputs if they were originally 0 (so 0 becomes 1)
    # Then computes AND of these flipped values
    # Then flips the result
    # So if original a[i]=0, b[i]=0: flip->1,1 -> AND->1 -> flip->0
    # If original a[i]=0, b[i]=1: flip->1, keep->1 -> AND->1 -> flip->0  
    # If original a[i]=1, b[i]=0: keep->0, flip->1 -> AND->0 -> flip->1
    # If original a[i]=1, b[i]=1: keep->0, keep->0 -> AND->0 -> flip->1
    # So: (0,0)->0, (0,1)->0, (1,0)->1, (1,1)->1
    # That's not OR! Let me recheck...
    
    # Original a=0, b=0: a[2-i]='0', so X(a[i]) -> a[i]=1; b[2-i]='0', so X(b[i]) -> b[i]=1; AND(1,1)=1; X(1)=0
    # Original a=0, b=1: a[2-i]='0' -> a[i]=1; b[2-i]='1' -> no X, b[i]=0; AND(1,0)=0; X(0)=1
    # Original a=1, b=0: a[2-i]='1' -> no X, a[i]=0; b[2-i]='0' -> X, b[i]=1; AND(0,1)=0; X(0)=1  
    # Original a=1, b=1: a[2-i]='1' -> no X, a[i]=0; b[2-i]='1' -> no X, b[i]=0; AND(0,0)=0; X(0)=1
    # So: (0,0)->0, (0,1)->1, (1,0)->1, (1,1)->1
    # Ah! That IS the OR operation!
    
    prog = pq.QProg()
    # Reset qubits - actually qvm initializes them to |0>
    # Set up the input based on the corrected understanding
    for i in range(3):
        if a_str[2-i] == '0':
            prog.insert(pq.X(qr_a[i]))
        if b_str[2-i] == '0':
            prog.insert(pq.X(qr_b[i]))
    
    # Compute AND of the flipped inputs
    for i in range(3):
        prog.insert(pq.TOFFOLI(qr_a[i], qr_b[i], ancillary[i]))
    
    # Flip the ancilla (giving us OR of original inputs)
    for i in range(3):
        prog.insert(pq.X(ancillary[i]))
    
    # Measure the ancilla register
    for i in range(3):
        prog.insert(pq.Measure(ancillary[i], cbits[i]))
    
    result = machine.run_with_configuration(prog, cbits, 1024)
    
    # Process results
    counts = result
    total = sum(counts.values())
    probs = {}
    for key, value in counts.items():
        # Ensure key is 3 bits, pad with leading zeros if necessary
        padded_key = key.zfill(3)[-3:]
        probs[padded_key] = value / total
        
    machine.finalize()
    
    return probs
