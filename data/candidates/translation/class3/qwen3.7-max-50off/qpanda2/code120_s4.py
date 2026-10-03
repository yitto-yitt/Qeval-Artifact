# EVAL_META: task_id=120, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(24)

def create_diagonal_circuit(diag):
    n = int(np.round(np.log2(len(diag))))
    q = qubits[:n]
    circ = pq.QCircuit()
    
    phases = [np.angle(d) for d in diag]
    a = phases.copy()
    h = 1
    while h < len(a):
        for i in range(0, len(a), h * 2):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h *= 2
        
    norm = 2 ** n
    
    for x in range(1, len(a)):
        angle = -2.0 * a[x] / norm
        if abs(angle) > 1e-12:
            support = [j for j in range(n) if (x & (1 << j))]
            target = support[-1]
            controls = support[:-1]
            
            for c in controls:
                circ << pq.CNOT(q[c], q[target])
                
            circ << pq.RZ(q[target], angle)
            
            for c in reversed(controls):
                circ << pq.CNOT(q[c], q[target])
                
    return circ

machine.finalize()
