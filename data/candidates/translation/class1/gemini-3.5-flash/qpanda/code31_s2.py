# EVAL_META: task_id=31, framework=qpanda, class=1
import pyqpanda3.core as pq

def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    machine.set_random_engine_seed(42)
    
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) \
         << pq.CNOT(q[0], q[1]) \
         << pq.Measure(q[0], c[0]) \
         << pq.Measure(q[1], c[1])
         
    result = machine.run_with_configuration(prog, c, 1024)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
