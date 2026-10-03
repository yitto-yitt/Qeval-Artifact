# EVAL_META: task_id=92, framework=qpanda2, class=1
import pyqpanda as pq

def calculate_stabilizer_state_info():
    qvm = pq.CPUQVM()
    qvm.init()
    q = qvm.qAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    qvm.run(prog)
    state = qvm.get_qState()
    
    probs = {}
    for i in range(4):
        b = format(i, '02b')
        probs[b] = abs(state[i])**2
        
    return probs
