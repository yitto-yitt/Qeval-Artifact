# EVAL_META: task_id=31, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def sampler_qiskit():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.Measure(qubits[0], cbits[0])
    prog << pq.Measure(qubits[1], cbits[1])
    
    shots = 4000
    config = {
        "shots": shots,
        "seed": 42
    }
    
    counts = qvm.run_with_configuration(prog, config)
    
    total = builtins.sum(counts.values())
    if total == 0:
        total = shots
        
    return {str(k): v / total for k, v in counts.items()}
