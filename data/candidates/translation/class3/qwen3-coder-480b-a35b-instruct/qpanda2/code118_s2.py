# EVAL_META: task_id=118, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    prog = pq.QProg()
    # In pyQPanda, we need to decompose C3SX gate manually
    # C3SX is a 4-qubit gate where 3 control qubits apply X gate to target when all controls are 1
    
    # We'll use Toffoli gates and additional ancilla logic to build C3SX
    # First, we need an additional ancilla qubit for construction
    ancilla = machine.qAlloc()
    
    # Build C3SX using two Toffoli gates
    # Step 1: Apply Toffoli on first two controls and ancilla
    prog << pq.TOFFOLI(qubits[0], qubits[1], ancilla)
    # Step 2: Apply Toffoli on third control, ancilla and target (qubit 3)
    prog << pq.TOFFOLI(qubits[2], ancilla, qubits[3])
    # Step 3: Uncompute the ancilla
    prog << pq.TOFFOLI(qubits[0], qubits[1], ancilla)
    
    # Clean up ancilla
    machine.qFree(ancilla)
    
    return prog

result = create_c3sx_circuit()
machine.finalize()
