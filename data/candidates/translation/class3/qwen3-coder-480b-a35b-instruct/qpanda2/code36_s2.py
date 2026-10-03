# EVAL_META: task_id=36, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)  # Allocate enough qubits for any reasonable input

def bv_function(s):
    n = len(s)
    # We need n+1 qubits (n for input, 1 for ancilla)
    circuit = pq.QProg()
    
    # Create a mapping for the qubits we'll use
    used_qubits = qubits[:n+1]
    
    # Apply CNOT gates based on the bitstring s
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit.insert(pq.CNOT(used_qubits[index], used_qubits[n]))
    
    return circuit

machine.finalize()
