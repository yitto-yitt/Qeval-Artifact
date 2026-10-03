# EVAL_META: task_id=120, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()

def cu1(prog, controls, target, theta):
    if abs(theta) < 1e-12:
        return
    if len(controls) == 0:
        prog << pq.U1(target, theta)
    elif len(controls) == 1:
        c = controls[0]
        prog << pq.U1(c, theta/2)
        prog << pq.U1(target, theta/2)
        prog << pq.CNOT(c, target)
        prog << pq.U1(target, -theta/2)
        prog << pq.CNOT(c, target)
    else:
        c1 = controls[-1]
        c2 = controls[-2]
        rest = controls[:-2]
        
        cu1(prog, rest + [c1], target, theta/2)
        prog << pq.CNOT(c2, c1)
        cu1(prog, rest + [c1], target, -theta/2)
        prog << pq.CNOT(c2, c1)
        cu1(prog, rest + [c2], target, theta/2)

def create_diagonal_circuit(diag):
    n = int(np.round(np.log2(len(diag))))
    prog = pq.QProg()
    
    if n == 0:
        return prog

    qubits = machine.qAlloc_many(n)
    phases = np.angle(diag)
    N = len(diag)
    
    theta = phases.copy()
    for i in range(n):
        for mask in range(N):
            if (mask & (1 << i)):
                theta[mask] -= theta[mask ^ (1 << i)]
                
    for mask in range(1, N):
        angle = theta[mask]
        if abs(angle) > 1e-12:
            subset_qubits = []
            for i in range(n):
                if (mask & (1 << i)):
                    subset_qubits.append(qubits[i])
            
            target = subset_qubits[-1]
            controls = subset_qubits[:-1]
            
            cu1(prog, controls, target, angle)
            
    return prog

machine.finalize()
