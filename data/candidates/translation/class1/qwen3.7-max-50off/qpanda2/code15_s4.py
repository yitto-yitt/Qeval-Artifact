# EVAL_META: task_id=15, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def noisy_bell():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    prog << pq.measure_all(q, c)
    
    counts = machine.run_with_configuration(prog, c, 1000)
    total = builtins.sum(counts.values())
    
    return {key: value / total for key, value in counts.items()}
