# EVAL_META: task_id=56, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def not_gate(a):
    machine = CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(8)
    cbits = machine.cAlloc_many(8)
    
    prog = QProg()
    
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7-i] == "0":
            prog << X(qubits[i])
    
    for i in range(8):
        prog << measure(qubits[i], cbits[i])
    
    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
