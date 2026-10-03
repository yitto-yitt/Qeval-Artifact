# EVAL_META: task_id=130, framework=qpanda, class=3
import pyqpanda3.core as pq

def inv_circuit(n):
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(n)
    prog = pq.QProg()
    
    # Apply Hadamard gates to the second and third qubits (index 1 and 2)
    for i in range(2):
        prog.insert(pq.H(qubits[i+1]))
    
    # Apply CNOT gates between the second and fourth qubits, and between the third and fifth qubits
    for i in range(2):
        prog.insert(pq.CNOT(qubits[i+1], qubits[i+2+1]))
    
    # Get the inverse of the program
    inv_prog = pq.get_inverse(prog)
    
    return inv_prog
