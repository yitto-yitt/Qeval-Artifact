# EVAL_META: task_id=118, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_c3sx_circuit():
    qvm = pq.QVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(4)
    
    # In pyQPanda3, we need to decompose C3SX gate manually
    # C3SX is a 3-controlled sqrt-X gate, which can be built using Toffoli gates and single-qubit gates
    
    # First apply Hadamard to target qubit (q[3])
    qvm << pq.H(q[3])
    
    # Apply Toffoli gates controlled by q[0], q[1], q[2] on ancilla and then on target
    # We need ancilla qubits for multi-control operations
    anc = qvm.qAlloc_many(2)  # Need 2 ancillas for 3-control operation
    
    # Decomposition of 3-controlled X gate using Toffoli gates
    qvm << pq.TOFFOLI(q[0], q[1], anc[0])
    qvm << pq.TOFFOLI(q[2], anc[0], anc[1])
    qvm << pq.TOFFOLI(q[0], q[1], anc[0])
    qvm << pq.TOFFOLI(q[2], anc[0], anc[1])
    
    # Apply S dagger to target qubit for C3SX (square root of X)
    qvm << pq.S(q[3]).dagger()
    
    # Reverse the Toffoli chain
    qvm << pq.TOFFOLI(q[2], anc[0], anc[1])
    qvm << pq.TOFFOLI(q[0], q[1], anc[0])
    qvm << pq.TOFFOLI(q[2], anc[0], anc[1])
    qvm << pq.TOFFOLI(q[0], q[1], anc[0])
    
    # Apply final H gate
    qvm << pq.H(q[3])
    
    # Get the circuit
    prog = qvm.get_circuit()
    
    # Free allocated qubits
    qvm.qFree_all([q, anc])
    
    return prog
