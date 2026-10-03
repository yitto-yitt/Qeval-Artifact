# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, X, Measure

def xor_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    
    prog = QProg()
    
    xor_val = a ^ b
    for i in range(8):
        if (xor_val >> i) & 1:
            prog << X(qubits[i])
    
    for i in range(8):
        prog << Measure(qubits[i], cbits[i])
    
    shots = 1000
    result = machine.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
