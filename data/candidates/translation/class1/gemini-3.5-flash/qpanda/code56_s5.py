# EVAL_META: task_id=56, framework=qpanda, class=1
import pyqpanda3.core as pq

def not_gate(a):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAllocMany(8)
    
    prog = pq.QProg()
    
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7-i] == "0":
            prog.insert(pq.X(qubits[i]))
            
    res = pq.prob_run_dict(prog, qubits, -1)
    
    # Filter out zero probabilities to return only the measured state(s)
    return {k: v for k, v in res.items() if v > 1e-6}
