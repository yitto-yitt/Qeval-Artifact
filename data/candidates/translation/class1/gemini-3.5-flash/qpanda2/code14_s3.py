# EVAL_META: task_id=14, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def bell_each_shot():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    prog << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    
    result = machine.run_with_configuration(prog, c, 10)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
