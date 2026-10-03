# EVAL_META: task_id=15, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def noisy_bell():
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    prog << pq.measure(q[0], c[0]) << pq.measure(q[1], c[1])
    
    result = qvm.run_with_configuration(prog, c, 1000)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
