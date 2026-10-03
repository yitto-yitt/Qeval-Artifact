# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def or_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(9)
    cbits = machine.cAlloc_many(3)
    a_qubits = qubits[0:3]
    b_qubits = qubits[3:6]
    anc_qubits = qubits[6:9]
    prog = QProg()
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    for i in range(3):
        if a_str[2-i] == '0':
            prog << X(a_qubits[i])
        if b_str[2-i] == '0':
            prog << X(b_qubits[i])
    for i in range(3):
        prog << Toffoli(a_qubits[i], b_qubits[i], anc_qubits[i])
    for i in range(3):
        prog << X(anc_qubits[i])
    for i in range(3):
        prog << Measure(anc_qubits[i], cbits[i])
    shots = 1024
    result = machine.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(result.values())
    return {k: v / total for k, v in result.items()}
