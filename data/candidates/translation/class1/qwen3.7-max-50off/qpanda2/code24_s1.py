# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq
import builtins
import inspect

def dj_algorithm(oracle):
    n = getattr(oracle, 'num_qubits', None)
    if n is None:
        n = getattr(oracle, 'n', 4)
        
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    
    prog = pq.QProg()
    prog << pq.X(qubits[n-1])
    for i in range(n):
        prog << pq.H(qubits[i])
        
    if callable(oracle):
        try:
            sig = inspect.signature(oracle)
            if len(sig.parameters) == 2:
                oracle_op = oracle(qvm, qubits)
            else:
                oracle_op = oracle(qubits)
        except Exception:
            oracle_op = oracle(qubits)
    else:
        oracle_op = oracle
        
    prog << oracle_op
    
    for i in range(n):
        prog << pq.H(qubits[i])
        
    c = qvm.cAlloc_many(n-1)
    for i in range(n-1):
        prog << pq.Measure(qubits[i], c[i])
        
    shots = 10000
    result = qvm.run_with_configuration(prog, c, shots)
    
    total = builtins.sum(result.values())
    if total == 0:
        return {}
    return {key: value / total for key, value in result.items()}
