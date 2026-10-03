# EVAL_META: task_id=130, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)  # Allocate more than enough qubits

def inv_circuit(n):
    prog = pq.QProg()
    qubits_local = qubits[:n]
    
    # Apply Hadamard gates to the second and third qubits (indices 1 and 2)
    for i in range(2):
        prog << pq.H(qubits_local[i + 1])
    
    # Apply CNOT gates between the second and fourth qubits, and between the third and fifth qubits
    for i in range(2):
        prog << pq.CNOT(qubits_local[i + 1], qubits_local[i + 2 + 1])
    
    # Return the inverse of the program
    return pq.get_inverse(prog)

machine.finalize()
