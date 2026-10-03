# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3.core as pq

def xor_gate(a, b):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    prog = pq.QProg()
    
    val = a ^ b
    for i in range(8):
        if (val >> i) & 1:
            prog << pq.X(qubits[i])
            
    # Get probability distribution with LSB-first ordering to match Qiskit
    result = qvm.prob_run_dict(prog, qubits[::-1])
    return result
