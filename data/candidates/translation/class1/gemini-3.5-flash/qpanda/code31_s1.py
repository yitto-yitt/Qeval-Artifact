# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import *

def sampler_qiskit():
    machine = CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    
    set_random_seed(42)
    
    result = machine.run_with_configuration(prog, c, 1024)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
