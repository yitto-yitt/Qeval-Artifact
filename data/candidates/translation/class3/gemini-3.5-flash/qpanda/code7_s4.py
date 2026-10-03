# EVAL_META: task_id=7, framework=qpanda, class=3
from pyqpanda3.core import *

def create_parametrized_gate():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc()
    
    vqc = VariationalQuantumCircuit()
    theta = var(0.0)
    vqc.insert(RX(q, theta))
    return vqc
