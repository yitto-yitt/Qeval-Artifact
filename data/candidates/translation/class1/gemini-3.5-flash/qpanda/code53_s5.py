# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3.core as pq

def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAllocMany(8)
    
    prog = pq.QProg()
    for i in range(8):
        if (a >> i) & 1:
            prog << pq.X(qubits[i])
        if (b >> i) & 1:
            prog << pq.X(qubits[i])
            
    q_list = [qubits[i] for i in reversed(range(8))]
    result = machine.prob_run_dict(prog, q_list)
    return {key: val for key, val in result.items() if val > 1e-6}
