# EVAL_META: task_id=1, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def run_bell_state_simulator():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    for i in range(2):
        prog << pq.Measure(qubits[i], cbits[i])
        
    counts = qvm.run_with_configuration(prog, cbits, 1000)
    qvm.finalize()
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
