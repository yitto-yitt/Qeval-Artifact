# EVAL_META: task_id=65, framework=qpanda2, class=3
import pyqpanda as pq
from numpy import pi

machine = pq.CPUQVM()
machine.init_qvm()
_max_qubits = 64
q = machine.qAlloc_many(_max_qubits)

def QFT(n):
    prog = pq.QProg()

    def qft_rotations(prog_obj, n_local):
        if n_local == 0:
            return
        n_local -= 1
        prog_obj << pq.H(q[n_local])
        for qubit in range(n_local):
            angle = pi / (2 ** (n_local - qubit))
            prog_obj << pq.CU(1.0, 0.0, 0.0, angle, q[qubit], q[n_local])
        qft_rotations(prog_obj, n_local)

    def swap_registers(prog_obj, n_local):
        for qubit in range(n_local // 2):
            prog_obj << pq.SWAP(q[qubit], q[n_local - qubit - 1])

    qft_rotations(prog, n)
    swap_registers(prog, n)
    machine.directly_run(prog)
    machine.finalize()
    return prog
