# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def visualize_bell_states():
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    
    prog_plus = pq.QProg()
    prog_plus.insert(pq.H(q[0]))
    prog_plus.insert(pq.CNOT(q[0], q[1]))
    prog_plus.insert(pq.measure_all(q, c))
    
    prog_minus = pq.QProg()
    prog_minus.insert(pq.X(q[0]))
    prog_minus.insert(pq.H(q[0]))
    prog_minus.insert(pq.CNOT(q[0], q[1]))
    prog_minus.insert(pq.measure_all(q, c))
    
    shots = 1000
    
    counts_plus = pq.run_with_configuration(prog_plus, qvm, shots)
    counts_minus = pq.run_with_configuration(prog_minus, qvm, shots)
    
    total_plus = builtins.sum(counts_plus.values())
    total_minus = builtins.sum(counts_minus.values())
    
    prob_plus = {k: v / total_plus for k, v in counts_plus.items()}
    prob_minus = {k: v / total_minus for k, v in counts_minus.items()}
    
    qvm.finalize()
    
    return {
        "phi_plus": prob_plus,
        "phi_minus": prob_minus
    }
