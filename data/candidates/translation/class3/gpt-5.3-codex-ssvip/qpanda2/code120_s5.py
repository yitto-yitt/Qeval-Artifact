# EVAL_META: task_id=120, framework=qpanda2, class=3
import math
import cmath
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_qpool = machine.qAlloc_many(32)

def create_diagonal_circuit(diag):
    n = int(round(math.log2(len(diag))))
    if (1 << n) != len(diag):
        raise ValueError("Length of diag must be a power of 2.")
    q = _qpool[:n]
    prog = pq.QProg()
    for idx, val in enumerate(diag):
        amp = complex(val)
        if abs(amp) == 0:
            raise ValueError("Diagonal elements must be non-zero for phase decomposition.")
        phase = cmath.phase(amp)
        if abs(phase) < 1e-12:
            continue
        controls = []
        for b in range(n):
            bit = (idx >> b) & 1
            if bit == 0:
                prog << pq.X(q[b])
            else:
                controls.append(q[b])
        target = controls[-1] if controls else q[0]
        if controls:
            ctrl_qubits = controls[:-1]
            if ctrl_qubits:
                prog << pq.U1(target, phase).control(ctrl_qubits)
            else:
                prog << pq.U1(target, phase)
        else:
            prog << pq.U1(target, phase)
        for b in range(n):
            bit = (idx >> b) & 1
            if bit == 0:
                prog << pq.X(q[b])
    machine.directly_run(prog)
    machine.finalize()
    return prog
