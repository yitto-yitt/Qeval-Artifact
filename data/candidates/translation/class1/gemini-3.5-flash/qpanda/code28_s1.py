# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq

def visualize_bell_states():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    # Phi plus
    prog_plus = pq.QProg()
    prog_plus << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    
    # Phi minus
    prog_minus = pq.QProg()
    prog_minus << pq.X(q[0]) << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    
    shots = 1000
    counts_plus = machine.run_with_configuration(prog_plus, c, shots)
    counts_minus = machine.run_with_configuration(prog_minus, c, shots)
    
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    prob_plus = {k: v / total_plus for k, v in counts_plus.items()}
    prob_minus = {k: v / total_minus for k, v in counts_minus.items()}
    
    machine.finalize()
    
    return {
        "phi_plus": prob_plus,
        "phi_minus": prob_minus
    }
