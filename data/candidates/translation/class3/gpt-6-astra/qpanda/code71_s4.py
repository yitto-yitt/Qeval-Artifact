# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import QProg, CPUQVM, H, T, CNOT, I

def create_quantum_circuit_based_h0_csx01_h1():
    prog = QProg()
    prog << I(2)
    prog << H(0)
    prog << H(1)
    prog << T(0) << T(1)
    prog << CNOT(0, 1)
    for _ in range(7):
        prog << T(1)
    prog << CNOT(0, 1)
    prog << H(1)
    prog << H(1)

    simulator = CPUQVM()
    simulator.run(prog, 1)
    return prog
