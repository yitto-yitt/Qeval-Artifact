# EVAL_META: task_id=40, framework=qpanda, class=1
import pyqpanda3.core as pq

def init_random_3qubit(desired_vector):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    state = [complex(x) for x in desired_vector]
    circuit = pq.amplitude_encode(qubits, state)
    
    prog = pq.QProg()
    prog << circuit
    for q, c in zip(qubits, cbits):
        prog << pq.Measure(q, c)
        
    counts = qvm.run_with_configuration(prog, cbits, 10000)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
