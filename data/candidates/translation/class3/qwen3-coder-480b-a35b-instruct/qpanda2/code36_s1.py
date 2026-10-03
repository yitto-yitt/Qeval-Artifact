# EVAL_META: task_id=36, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)  # Allocate enough qubits for any reasonable input

def bv_function(s):
    n = len(s)
    # Create a new quantum program for this specific circuit
    prog = pq.QProg()
    
    # Use the first n+1 qubits for this circuit
    circuit_qubits = qubits[:n+1]
    
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog.insert(pq.CNOT(circuit_qubits[index], circuit_qubits[n]))
    
    return prog

machine.finalize()
