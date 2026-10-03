# EVAL_META: task_id=36, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)  # Allocate enough qubits for any reasonable input

def bv_function(s):
    n = len(s)
    # Need to allocate new qubits for this specific circuit
    local_qubits = machine.qAlloc_many(n + 1)
    
    prog = pq.QProg()
    
    # Reverse the string s to match the Qiskit indexing
    reversed_s = s[::-1]
    
    for index, bit in enumerate(reversed_s):
        if bit == "1":
            prog.insert(pq.CNOT(local_qubits[index], local_qubits[n]))
    
    return prog, local_qubits

# Manual cleanup
machine.finalize()
