# EVAL_META: task_id=28, framework=qpanda, class=1
import pyqpanda3.core as pq

def visualize_bell_states():
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(4)
    c = machine.cAlloc_many(4)
    
    prog_plus = pq.QProg()
    prog_plus << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    prog_plus << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    
    prog_minus = pq.QProg()
    prog_minus << pq.X(q[2]) << pq.H(q[2]) << pq.CNOT(q[2], q[3])
    prog_minus << pq.Measure(q[2], c[2]) << pq.Measure(q[3], c[3])
    
    result_plus = machine.run_with_configuration(prog_plus, [c[0], c[1]], 1000)
    result_minus = machine.run_with_configuration(prog_minus, [c[2], c[3]], 1000)
    
    machine.finalize()
    
    total_plus = sum(result_plus.values())
    total_minus = sum(result_minus.values())
    
    return {
        "phi_plus": {key: val / total_plus for key, val in result_plus.items()},
        "phi_minus": {key: val / total_minus for key, val in result_minus.items()}
    }
