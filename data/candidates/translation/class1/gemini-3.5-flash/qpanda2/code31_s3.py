# EVAL_META: task_id=31, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    try:
        machine.set_random_seed(42)
    except:
        pass
    
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    prog << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    
    shots = 1024
    result = machine.run_with_configuration(prog, c, shots)
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
