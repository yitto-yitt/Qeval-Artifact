# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    prog << pq.init_state(q, desired_vector)
    
    for i in range(3):
        prog << pq.Measure(q[i], c[i])
        
    shots = 4000
    result = pq.run_with_configuration(prog, c, shots)
    
    total = builtins.sum(result.values())
    probs = {}
    for key, val in result.items():
        rev_key = key[::-1]
        probs[rev_key] = val / total
        
    machine.destroy()
    return probs
