# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import *

def create_c3sx_circuit():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(4)
    
    prog = QProg()
    gate = SX(qubits[3]).control([qubits[0], qubits[1], qubits[2]])
    prog << gate
    
    # Attach machine to prog to prevent garbage collection
    prog.machine = machine
    return prog
