# EVAL_META: task_id=14, framework=qpanda, class=1
try:
    import pyqpanda3.core as pq
except ImportError:
    import pyqpanda as pq

def bell_each_shot():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    
    result = machine.run_with_configuration(prog, c, 10)
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
