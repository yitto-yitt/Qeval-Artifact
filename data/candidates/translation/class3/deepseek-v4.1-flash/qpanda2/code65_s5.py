# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

machine = CPUQVM()
machine.init_qvm()
_qubits = []

def QFT(n):
    qubits = machine.qAlloc_many(n)
    _qubits.extend(qubits)
    prog = QProg()
    def qft_rotations(prog, n):
        if n == 0:
            return
        n -= 1
        prog << H(qubits[n])
        for qubit in range(n):
            angle = pi / (2 ** (n - qubit))
            prog << CP(qubits[qubit], qubits[n], angle)
        qft_rotations(prog, n)
    qft_rotations(prog, n)
    for qubit in range(n // 2):
        prog << SWAP(qubits[qubit], qubits[n - qubit - 1])
    return prog

if __name__ == "__main__":
    machine.finalize()
