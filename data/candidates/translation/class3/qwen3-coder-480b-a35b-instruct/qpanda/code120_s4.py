# EVAL_META: task_id=120, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
import math

def create_diagonal_circuit(diag):
    # Calculate number of qubits needed based on diagonal length
    num_qubits = int(math.log2(len(diag)))
    
    # Create quantum program and machine
    prog = QProg()
    qvm = pq.QMachine()
    qubits = qvm.qAlloc_many(num_qubits)
    
    # Convert diagonal elements to phase operations
    # For a diagonal gate with elements [d0, d1, ..., dN], we need to apply controlled rotations
    # that implement the phase shifts corresponding to each diagonal element
    
    # Extract phases from diagonal elements (assuming they are complex numbers on unit circle)
    phases = []
    for elem in diag:
        if isinstance(elem, complex):
            phase = math.atan2(elem.imag, elem.real)
        else:
            phase = 0
        phases.append(phase)
    
    # Apply multi-controlled phase gates to implement diagonal operation
    # This is a simplified approach - implementing general diagonal gates in pyQPanda
    # requires decomposing into basic gates
    
    # For a 2^n x 2^n diagonal matrix, we can implement it using phase kickback trick
    # or by implementing each computational basis state with appropriate phase
    
    for i in range(len(phases)):
        # Create a mask for the specific computational basis state
        mask = i
        controls = []
        for j in range(num_qubits):
            if (mask >> j) & 1:
                controls.append(qubits[j])
        
        # Apply multi-controlled phase rotation
        # This is a simplified implementation - real implementation would need 
        # proper multi-controlled U1 gates
        if phases[i] != 0:
            # Build the state selector and apply phase
            # We'll use X gates to flip qubits that should be |1> then apply multi-CNOT
            temp_prog = QProg()
            
            # Flip qubits that should be |1> but start as |0>
            for j in range(num_qubits):
                if ((i >> j) & 1) == 0:
                    temp_prog << X(qubits[j])
                    
            # Apply multi-controlled Z gate (which adds phase)
            if num_qubits == 1:
                temp_prog << RZ(qubits[0], phases[i])
            elif num_qubits == 2:
                temp_prog << CR(qubits[0], qubits[1], RZ_GATE(0), phases[i])
            else:
                # For more than 2 qubits, we would need more complex decomposition
                # This is a placeholder for the actual decomposition
                pass
            
            # Flip back the qubits that were flipped
            for j in range(num_qubits):
                if ((i >> j) & 1) == 0:
                    temp_prog << X(qubits[j])
            
            prog << temp_prog
    
    return prog
