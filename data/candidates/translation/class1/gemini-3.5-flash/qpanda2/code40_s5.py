# EVAL_META: task_id=40, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def init_random_3qubit(desired_vector):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = pq.QProg()
    state_list = [complex(x) for x in desired_vector]
    encode_cir = pq.amplitude_encode(qubits, state_list)
    prog << encode_cir
    
    for i in range(3):
        prog << pq.Measure(qubits[i], cbits[i])
        
    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
