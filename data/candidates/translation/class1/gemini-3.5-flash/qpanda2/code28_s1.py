# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def visualize_bell_states():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    # Phi+ state
    prog_plus = pq.QProg()
    prog_plus << pq.H(q[0]) \
              << pq.CNOT(q[0], q[1]) \
              << pq.Measure(q[0], c[0]) \
              << pq.Measure(q[1], c[1])
              
    # Phi- state
    prog_minus = pq.QProg()
    prog_minus << pq.X(q[0]) \
               << pq.H(q[0]) \
               << pq.CNOT(q[0], q[1]) \
               << pq.Measure(q[0], c[0]) \
               << pq.Measure(q[1], c[1])
               
    result_plus = machine.run_with_configuration(prog_plus, c, 1000)
    result_minus = machine.run_with_configuration(prog_minus, c, 1000)
    
    plus_total = builtins.sum(result_plus.values())
    minus_total = builtins.sum(result_minus.values())
    
    phi_plus_dist = {key: value / plus_total for key, value in result_plus.items()}
    phi_minus_dist = {key: value / minus_total for key, value in result_minus.items()}
    
    machine.finalize()
    
    return {
        "phi_plus": phi_plus_dist,
        "phi_minus": phi_minus_dist
    }
