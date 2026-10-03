# EVAL_META: task_id=130, framework=qpanda, class=3
from pyqpanda3.core import *

def inv_circuit(n):
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    
    circuit = QCircuit()
    for i in range(2):
        circuit << H(q[i+1])

    for i in range(2):
        circuit << CNOT(q[i+1], q[i+3])
    
    prog = QProg()
    prog << circuit.dagger()
    return prog
