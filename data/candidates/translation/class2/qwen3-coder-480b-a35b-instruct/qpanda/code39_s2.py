# EVAL_META: task_id=39, framework=qpanda, class=2
import pyqpanda3 as pq
from pyqpanda3.core import *

def create_uniform_superposition(n):
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(n)
    
    prog = QProg()
    for i in range(n):
        prog << H(qubits[i])
    
    statevector = machine.get_state_vector(prog)
    destroy_quantum_machine(machine)
    return statevector
