# EVAL_META: task_id=90, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_custom_controlled():
    # Create the base operation: X on qubit 0, H on qubit 1
    qvec_base = machine.qAlloc_many(2)
    prog_base = pq.QProg()
    prog_base << pq.X(qvec_base[0]) << pq.H(qvec_base[1])
    
    # Convert to a custom gate (in pyQPanda we use QProg directly)
    # For controlled version, we need to manually construct the controlled operations
    prog_final = pq.QProg()
    
    # Apply controlled-X from qubits 0 and 3 to qubit 1
    prog_final << pq.Toffoli(qubits[0], qubits[3], qubits[1])
    
    # Apply controlled-H from qubits 0 and 3 to qubit 2
    # Since H is its own inverse and can be controlled via Toffoli + H transformations,
    # we'll implement it as a controlled operation
    # Using ancilla-free implementation for CH
    prog_final << pq.RZ(qubits[2], -pq.PI/2)
    prog_final << pq.CNOT(qubits[0], qubits[2])
    prog_final << pq.RZ(qubits[2], pq.PI/2)
    prog_final << pq.CNOT(qubits[3], qubits[2])
    prog_final << pq.RZ(qubits[2], -pq.PI/2)
    prog_final << pq.CNOT(qubits[0], qubits[2])
    prog_final << pq.RZ(qubits[2], pq.PI/2)
    
    return prog_final

result = create_custom_controlled()
machine.finalize()
