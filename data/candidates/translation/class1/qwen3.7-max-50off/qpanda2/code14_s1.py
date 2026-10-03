# EVAL_META: task_id=14, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def bell_each_shot():
    qmachine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qmachine.qAlloc_many(2)
    c = qmachine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0])
    prog << pq.CNOT(q[0], q[1])
    prog << pq.measure(q[0], c[0])
    prog << pq.measure(q[1], c[1])
    
    counts = pq.run_with_configuration(prog, c, 10)
    total = builtins.sum(counts.values())
    
    probs = {key: value / total for key, value in counts.items()}
    
    qmachine.finalize()
    return probs
