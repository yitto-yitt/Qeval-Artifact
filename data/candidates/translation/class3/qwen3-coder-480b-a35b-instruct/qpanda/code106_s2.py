# EVAL_META: task_id=106, framework=qpanda, class=3
import pyqpanda3.core as pq


def compose_cnot_dihedral():
    # Create two quantum programs
    prog1 = pq.QProg()
    qvec1 = pq.QVec(2)
    
    # Add gates to first program: CX(0,1) and T(0)
    prog1.insert(pq.CNOT(qvec1[0], qvec1[1]))
    prog1.insert(pq.T(qvec1[0]))
    
    # Create second program as copy of first plus X(1)
    prog2 = pq.QProg()
    qvec2 = pq.QVec(2)
    
    # Add same gates as first program
    prog2.insert(pq.CNOT(qvec2[0], qvec2[1]))
    prog2.insert(pq.T(qvec2[0]))
    # Add additional X gate on qubit 1
    prog2.insert(pq.X(qvec2[1]))
    
    # Convert to CNOTDihedral-like elements if available in pyqpanda3
    # Since pyqpanda3 doesn't have direct CNOTDihedral equivalent,
    # we work with the programs directly
    # However, following the pattern from the original task
    
    # In pyQPanda3, we may need to use different representation
    # Based on the API structure, we'll create the composition manually
    composed_prog = pq.QProg()
    qvec_comp = pq.QVec(2)
    
    # Compose the two programs by inserting both
    temp_prog1 = pq.QProg()
    temp_qvec1 = pq.QVec(2)
    temp_prog1.insert(pq.CNOT(temp_qvec1[0], temp_qvec1[1]))
    temp_prog1.insert(pq.T(temp_qvec1[0]))
    
    temp_prog2 = pq.QProg()
    temp_qvec2 = pq.QVec(2)
    temp_prog2.insert(pq.CNOT(temp_qvec2[0], temp_qvec2[1]))
    temp_prog2.insert(pq.T(temp_qvec2[0]))
    temp_prog2.insert(pq.X(temp_qvec2[1]))
    
    # Create the composed program
    composed_prog.insert(pq.CNOT(qvec_comp[0], qvec_comp[1]))
    composed_prog.insert(pq.T(qvec_comp[0]))
    composed_prog.insert(pq.CNOT(qvec_comp[0], qvec_comp[1]))
    composed_prog.insert(pq.T(qvec_comp[0]))
    composed_prog.insert(pq.X(qvec_comp[1]))
    
    # Return the composed program (as closest equivalent to CNOTDihedral composition)
    return composed_prog
