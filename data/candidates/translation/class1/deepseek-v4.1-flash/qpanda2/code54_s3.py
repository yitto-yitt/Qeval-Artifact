# EVAL_META: task_id=54, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def and_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    
    qubits = qvm.qAlloc_many(9)
    qr_a = qubits[0:3]
    qr_b = qubits[3:6]
    ancillary = qubits[6:9]
    
    cbits = qvm.cAlloc_many(3)
    prog = QProg()
    
    for i in range(3):
        if (a >> i) & 1:
            prog << X(qr_a[i])
        if (b >> i) & 1:
            prog << X(qr_b[i])
    
    for i in range(3):
        prog << Toffoli(qr_a[i], qr_b[i], ancillary[i])
    
    prog << Measure(ancillary[2], cbits[0])
    prog << Measure(ancillary[1], cbits[1])
    prog << Measure(ancillary[0], cbits[2])
    
    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
