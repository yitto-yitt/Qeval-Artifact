# EVAL_META: task_id=40, framework=qpanda, class=1
import pyqpanda3.core as pq

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    val_list = [complex(x) for x in desired_vector]
    prog << pq.amplitude_encode(q, val_list)
    
    for i in range(3):
        prog << pq.Measure(q[i], c[i])
        
    result = machine.run_with_configuration(prog, c, 1024)
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
