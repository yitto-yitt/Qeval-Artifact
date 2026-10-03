# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import *

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0])
    prog << RZ(q[1], theta).control([q[0]])
    prog << H(q[1])
    prog << RY(q[0], theta).control([q[1]])
    
    # Attach machine and qubits to the program to prevent garbage collection
    prog.machine = machine
    prog.qubits = q
    return prog
