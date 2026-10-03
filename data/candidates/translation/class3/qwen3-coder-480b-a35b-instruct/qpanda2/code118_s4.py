# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    # In pyQPanda, we need to decompose C3SX gate manually
    # C3SX is a 4-qubit gate where 3 control qubits apply X on target if all controls are 1
    # We'll use Toffoli gates and additional ancilla to construct this
    
    # Using ancilla qubit approach for multi-control gate
    # First create a circuit that computes AND of first three qubits
    # Then apply X on target controlled by the ancilla
    # Finally uncompute the ancilla
    
    # Allocate ancilla qubits (we need 2 additional qubits)
    ancillas = machine.qAlloc_many(2)
    
    # Step 1: Compute first two controls into ancilla[0]
    prog << pq.TOFFOLI(qubits[0], qubits[1], ancillas[0])
    
    # Step 2: Compute third control with previous result into ancilla[1]
    prog << pq.TOFFOLI(ancillas[0], qubits[2], ancillas[1])
    
    # Step 3: Apply X on target controlled by ancilla[1]
    prog << pq.CNOT(ancillas[1], qubits[3])
    
    # Step 4: Uncompute ancilla[1]
    prog << pq.TOFFOLI(ancillas[0], qubits[2], ancillas[1])
    
    # Step 5: Uncompute ancilla[0]
    prog << pq.TOFFOLI(qubits[0], qubits[1], ancillas[0])
    
    # Free ancilla qubits
    for q in ancillas:
        machine.qFree(q)
    
    return prog

# Clean up
machine.finalize()
