# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda import *

def xor_gate(a, b):
    init(QMachineType.CPU)
    qubits = qAlloc_many(8)
    cbits = cAlloc_many(8)
    
    prog = QProg()
    
    # Encode input a
    for i in range(8):
        if (a >> i) & 1:
            prog.insert(X(qubits[i]))
    
    # Apply XOR with b (classical XOR on each bit)
    for i in range(8):
        if (b >> i) & 1:
            prog.insert(X(qubits[i]))
    
    # Measure all qubits
    for i in range(8):
        prog.insert(Measure(qubits[i], cbits[i]))
    
    # Run the circuit
    result = run_with_configuration(prog, cbits, 1024)
    
    # Convert results to probability distribution
    total = sum(result.values())
    prob_dist = {}
    
    for key, value in result.items():
        # Reverse the bit string to match Qiskit's convention
        reversed_key = key[::-1]
        prob_dist[reversed_key] = value / total
    
    finalize()
    return prob_dist
