# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq

def bv_algorithm(s):
    n = len(s)
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qAlloc_many(n + 1)
    c = qvm.cAlloc_many(n)
    
    ancilla = n
    circ = pq.QCircuit()
    circ << pq.X(q[ancilla])
    for i in range(n + 1):
        circ << pq.H(q[i])
        
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circ << pq.CNOT(q[index], q[ancilla])
            
    for i in range(n):
        circ << pq.H(q[i])
        
    prog = pq.QProg()
    prog.insert(circ)
    for i in range(n):
        prog << pq.Measure(q[i], c[i])
        
    result = pq.run_with_configuration(prog, qvm, 1)
    bitstrings = list(result.keys())
    
    qvm.finalize()
    return [bitstrings, result]
