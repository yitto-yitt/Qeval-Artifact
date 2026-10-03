# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def dj_algorithm(oracle):
    if hasattr(oracle, 'num_qubits'):
        n = oracle.num_qubits
    elif hasattr(oracle, 'n'):
        n = oracle.n
    else:
        n = 3

    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    cbits = qvm.cAlloc_many(n - 1)

    prog = pq.QProg()
    prog << pq.X(qubits[n - 1])
    for q in qubits:
        prog << pq.H(q)
        
    if callable(oracle):
        try:
            prog << oracle(qubits)
        except TypeError:
            prog << oracle()
    elif hasattr(oracle, 'circuit'):
        prog << oracle.circuit
    else:
        prog << oracle

    for q in qubits:
        prog << pq.H(q)
        
    for i in range(n - 1):
        prog << pq.Measure(qubits[i], cbits[i])
        
    result = qvm.run_with_configuration(prog, cbits, 1024)
    total = builtins.sum(result.values())
    
    return {key: value / total for key, value in result.items()}
