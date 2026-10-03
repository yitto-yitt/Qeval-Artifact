# EVAL_META: task_id=65, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def QFT(n):
    prog = QCircuit()
    qs = qubits[:n]

    def qft_rotations(circuit, qlist, n):
        if n == 0:
            return
        n -= 1
        circuit << H(qlist[n])
        for qubit in range(n):
            circuit << CR(qlist[qubit], qlist[n], pi / 2 ** (n - qubit))
        qft_rotations(circuit, qlist, n)

    def swap_registers(circuit, qlist, n):
        for i in range(n // 2):
            circuit << SWAP(qlist[i], qlist[n - i - 1])

    qft_rotations(prog, qs, n)
    swap_registers(prog, qs, n)
    return prog

machine.finalize()
