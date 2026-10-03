# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda import *
from math import *

def or_gate(a, b):
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    machine = init(QMachineType.CPU)
    qubits = machine.qAlloc_many(9)
    cbits = machine.cAlloc_many(3)
    prog = QProg()
    for i in range(3):
        if a_bits[2-i] == '0':
            prog.insert(X(qubits[i]))
        if b_bits[2-i] == '0':
            prog.insert(X(qubits[i+3]))
    for i in range(3):
        prog.insert(X(qubits[i]))
        prog.insert(X(qubits[i+3]))
        prog.insert(X(qubits[i+6]))
        prog.insert(H(qubits[i+6]))
        prog.insert(CNOT(qubits[i], qubits[i+6]))
        prog.insert(CNOT(qubits[i+3], qubits[i+6]))
        prog.insert(H(qubits[i+6]))
        prog.insert(X(qubits[i]))
        prog.insert(X(qubits[i+3]))
        prog.insert(X(qubits[i+6]))
    for i in range(3):
        prog.insert(Measure(qubits[i+6], cbits[i]))
    machine.directly_run(prog)
    result = machine.get_prob_dict([cbits[0], cbits[1], cbits[2]])
    machine.finalize()
    return result
