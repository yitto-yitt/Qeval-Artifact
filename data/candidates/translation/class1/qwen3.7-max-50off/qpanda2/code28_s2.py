# EVAL_META: task_id=28, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def visualize_bell_states():
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    
    q_plus = qvm.qAlloc_many(2)
    c_plus = qvm.cAlloc_many(2)
    prog_plus = pq.QProg()
    prog_plus << pq.H(q_plus[0]) \
              << pq.CNOT(q_plus[0], q_plus[1])
    for i in range(2):
        prog_plus << pq.Measure(q_plus[i], c_plus[i])
        
    q_minus = qvm.qAlloc_many(2)
    c_minus = qvm.cAlloc_many(2)
    prog_minus = pq.QProg()
    prog_minus << pq.X(q_minus[0]) \
               << pq.H(q_minus[0]) \
               << pq.CNOT(q_minus[0], q_minus[1])
    for i in range(2):
        prog_minus << pq.Measure(q_minus[i], c_minus[i])
        
    shots = 1000
    result_plus = pq.run_with_configuration(prog_plus, qvm, shots)
    result_minus = pq.run_with_configuration(prog_minus, qvm, shots)
    
    total_plus = builtins.sum(result_plus.values())
    total_minus = builtins.sum(result_minus.values())
    
    prob_plus = {k: v / total_plus for k, v in result_plus.items()}
    prob_minus = {k: v / total_minus for k, v in result_minus.items()}
    
    return {
        "phi_plus": prob_plus,
        "phi_minus": prob_minus
    }
