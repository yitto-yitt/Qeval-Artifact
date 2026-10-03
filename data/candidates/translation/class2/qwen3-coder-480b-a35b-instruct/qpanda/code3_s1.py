# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda import *


def create_ghz(drawing=False):
    machine = init(QMachineType.CPU)
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    prog = QProg()
    prog.insert(H(qubits[0]))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(CNOT(qubits[0], qubits[2]))
    
    for i in range(3):
        prog.insert(Measure(qubits[i], cbits[i]))
    
    if drawing:
        # pyQPanda doesn't have built-in circuit drawing like Qiskit
        # Returning just the program object as drawing capability is limited
        return prog, str(prog)
    
    return prog
