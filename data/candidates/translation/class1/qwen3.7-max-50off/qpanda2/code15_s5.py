# EVAL_META: task_id=15, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def noisy_bell():
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    prog = pq.QProg()
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.measure(qubits[0], cbits[0])
    prog << pq.measure(qubits[1], cbits[1])
    
    result = qvm.run_with_configuration(prog, cbits, 1000)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
