# EVAL_META: task_id=56, framework=qpanda2, class=1
import pyqpanda as pq

def not_gate(a):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(8)
    prog = pq.QProg()
    
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7-i] == "0":
            prog << pq.X(qubits[i])
            
    qubit_list = [qubits[i] for i in range(7, -1, -1)]
    res = machine.prob_run_dict(prog, qubit_list)
    
    # Filter out zero probabilities to match the sampling output
    return {k: v for k, v in res.items() if v > 0}
