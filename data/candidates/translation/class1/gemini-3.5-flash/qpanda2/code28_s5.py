# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def visualize_bell_states():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    # phi_plus
    q_plus = machine.qAlloc_many(2)
    c_plus = machine.cAlloc_many(2)
    
    prog_plus = pq.QProg()
    prog_plus << pq.H(q_plus[0]) \
              << pq.CNOT(q_plus[0], q_plus[1]) \
              << pq.Measure(q_plus[0], c_plus[0]) \
              << pq.Measure(q_plus[1], c_plus[1])
              
    # phi_minus
    q_minus = machine.qAlloc_many(2)
    c_minus = machine.cAlloc_many(2)
    
    prog_minus = pq.QProg()
    prog_minus << pq.X(q_minus[0]) \
               << pq.H(q_minus[0]) \
               << pq.CNOT(q_minus[0], q_minus[1]) \
               << pq.Measure(q_minus[0], c_minus[0]) \
               << pq.Measure(q_minus[1], c_minus[1])
               
    shots = 1000
    result_plus = machine.run_with_configuration(prog_plus, shots)
    result_minus = machine.run_with_configuration(prog_minus, shots)
    
    machine.finalize()
    
    plus_total = builtins.sum(result_plus.values())
    minus_total = builtins.sum(result_minus.values())
    
    return {
        "phi_plus": {key: val / plus_total for key, val in result_plus.items()},
        "phi_minus": {key: val / minus_total for key, val in result_minus.items()}
    }
