# EVAL_META: task_id=36, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)  # Allocate enough qubits for any reasonable input

def bv_function(s):
    n = len(s)
    # Create a new quantum program for this specific circuit
    prog = pq.QProg()
    qubits_local = machine.qAlloc_many(n + 1)
    
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog.insert(pq.CNOT(qubits_local[index], qubits_local[n]))
    
    # Return the program - though pyQPanda doesn't have direct oracle objects like Qiskit
    # we return the program that implements the oracle behavior
    return prog

machine.finalize()
