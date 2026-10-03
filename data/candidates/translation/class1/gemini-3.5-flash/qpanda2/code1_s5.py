# EVAL_META: task_id=1, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def run_bell_state_simulator():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    prog << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    
    result = machine.run_with_configuration(prog, c, 1000)
    
    total = builtins.sum(result.values())
    probs = {key: value / total for key, value in result.items()}
    
    machine.finalize()
    return probs
