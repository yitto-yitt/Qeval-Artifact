# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import *

def create_parametrized_gate():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qalloc_many(1)
    
    vqc = VariationalQuantumCircuit()
    theta = var(0.0, True)
    vqc.insert(VariationalQuantumGate_RX(q[0], theta))
    
    return vqc
