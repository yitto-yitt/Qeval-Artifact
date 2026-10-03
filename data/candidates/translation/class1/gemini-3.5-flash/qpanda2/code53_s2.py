# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    
    prog = pq.QProg()
    
    # Apply X gates for a
    for i in range(8):
        if (a >> i) & 1:
            prog << pq.X(qubits[i])
            
    # Apply X gates for b
    for i in range(8):
        if (b >> i) & 1:
            prog << pq.X(qubits[i])
            
    # Measure qubits to classical bits
    # Mapping qubit i to cbit 7-i to match Qiskit's little-endian representation
    for i in range(8):
        prog << pq.Measure(qubits[i], cbits[7 - i])
        
    shots = 1000
    result = machine.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(result.values())
    probabilities = {key: val / total for key, val in result.items()}
    
    machine.finalize()
    return probabilities
