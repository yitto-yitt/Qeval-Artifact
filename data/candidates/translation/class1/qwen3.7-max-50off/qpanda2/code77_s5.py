# EVAL_META: task_id=77, framework=qpanda2, class=1
import math
import builtins
import pyqpanda as pq

def circuit_from_probability_dist(probability_dist):
    num_qubits = math.ceil(math.log2(max(probability_dist.keys()) + 1)) or 1
    amplitudes = []
    for basis_state in range(2**num_qubits):
        prob = probability_dist.get(basis_state, 0)
        amplitudes.append(math.sqrt(prob))
        
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    qubits = qvm.qAlloc_many(num_qubits)
    prog = pq.QProg()
    
    def prepare_recursive(progs, qs, amps, ctrls, cstates):
        n = len(qs)
        norm = math.sqrt(builtins.sum(a**2 for a in amps))
        if norm < 1e-12:
            return
            
        if n == 1:
            a0 = amps[0] / norm
            a0 = max(-1.0, min(1.0, a0))
            theta = 2 * math.acos(a0)
            if abs(theta) > 1e-12:
                gate = pq.RY(qs[0], theta)
                if ctrls:
                    for i, st in enumerate(cstates):
                        if st == 0:
                            progs << pq.X(ctrls[i])
                    progs << gate.control(ctrls)
                    for i, st in enumerate(cstates):
                        if st == 0:
                            progs << pq.X(ctrls[i])
                else:
                    progs << gate
            return
            
        half = 2**(n-1)
        v0 = amps[:half]
        v1 = amps[half:]
        
        norm0 = math.sqrt(builtins.sum(a**2 for a in v0))
        norm1 = math.sqrt(builtins.sum(a**2 for a in v1))
        
        a0 = norm0 / norm
        a0 = max(-1.0, min(1.0, a0))
        theta = 2 * math.acos(a0)
        
        target_q = qs[-1]
        rest_q = qs[:-1]
        
        if abs(theta) > 1e-12:
            gate = pq.RY(target_q, theta)
            if ctrls:
                for i, st in enumerate(cstates):
                    if st == 0:
                        progs << pq.X(ctrls[i])
                progs << gate.control(ctrls)
                for i, st in enumerate(cstates):
                    if st == 0:
                        progs << pq.X(ctrls[i])
            else:
                progs << gate
                
        if norm0 > 1e-12:
            prepare_recursive(progs, rest_q, v0, ctrls + [target_q], cstates + [0])
        if norm1 > 1e-12:
            prepare_recursive(progs, rest_q, v1, ctrls + [target_q], cstates + [1])

    prepare_recursive(prog, qubits, amplitudes, [], [])
    return prog
