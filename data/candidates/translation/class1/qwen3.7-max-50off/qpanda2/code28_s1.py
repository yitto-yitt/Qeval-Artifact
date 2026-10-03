# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def visualize_bell_states():
    qvm1 = pq.init_quantum_machine(pq.QMachineType.CPU)
    q1 = qvm1.qAlloc_many(2)
    c1 = qvm1.cAlloc_many(2)
    
    prog_plus = pq.QProg()
    prog_plus << pq.H(q1[0]) << pq.CNOT(q1[0], q1[1]) << pq.measure_all(q1, c1)
    counts_plus = pq.run_with_configuration(prog_plus, qvm1, 1000)
    
    qvm2 = pq.init_quantum_machine(pq.QMachineType.CPU)
    q2 = qvm2.qAlloc_many(2)
    c2 = qvm2.cAlloc_many(2)
    
    prog_minus = pq.QProg()
    prog_minus << pq.X(q2[0]) << pq.H(q2[0]) << pq.CNOT(q2[0], q2[1]) << pq.measure_all(q2, c2)
    counts_minus = pq.run_with_configuration(prog_minus, qvm2, 1000)
    
    total_plus = builtins.sum(counts_plus.values())
    total_minus = builtins.sum(counts_minus.values())
    
    return {
        "phi_plus": {k: v / total_plus for k, v in counts_plus.items()},
        "phi_minus": {k: v / total_minus for k, v in counts_minus.items()}
    }
