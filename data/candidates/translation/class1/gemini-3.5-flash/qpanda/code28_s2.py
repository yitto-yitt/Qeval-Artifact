# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq

def visualize_bell_states():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    # phi_plus
    q_plus = [machine.qAlloc() for _ in range(2)]
    c_plus = [machine.cAlloc() for _ in range(2)]
    
    prog_plus = pq.QProg()
    prog_plus << pq.H(q_plus[0])
    prog_plus << pq.CNOT(q_plus[0], q_plus[1])
    prog_plus << pq.Measure(q_plus[0], c_plus[0])
    prog_plus << pq.Measure(q_plus[1], c_plus[1])
    
    # phi_minus
    q_minus = [machine.qAlloc() for _ in range(2)]
    c_minus = [machine.cAlloc() for _ in range(2)]
    
    prog_minus = pq.QProg()
    prog_minus << pq.X(q_minus[0])
    prog_minus << pq.H(q_minus[0])
    prog_minus << pq.CNOT(q_minus[0], q_minus[1])
    prog_minus << pq.Measure(q_minus[0], c_minus[0])
    prog_minus << pq.Measure(q_minus[1], c_minus[1])
    
    counts_plus = machine.run_with_configuration(prog_plus, c_plus, 1000)
    counts_minus = machine.run_with_configuration(prog_minus, c_minus, 1000)
    
    machine.finalize()
    
    total_plus = sum(counts_plus.values())
    prob_plus = {k: v / total_plus for k, v in counts_plus.items()}
    
    total_minus = sum(counts_minus.values())
    prob_minus = {k: v / total_minus for k, v in counts_minus.items()}
    
    return {
        "phi_plus": prob_plus,
        "phi_minus": prob_minus
    }
