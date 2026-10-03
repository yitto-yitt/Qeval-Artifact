# EVAL_META: task_id=70, framework=qpanda, class=3
from pyqpanda3.core import QMachine, QProg, Qubit, H, CNOT, Toffoli, SDG

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    machine = QMachine()
    q = machine.qAlloc_many(3)
    prog = QProg()

    # H(0)
    prog << H(q[0])

    # CSWAP(0,1,2) decomposed as CNOT(2,1) + Toffoli(0,1,2) + CNOT(2,1)
    prog << CNOT(q[2], q[1])
    prog << Toffoli(q[0], q[1], q[2])
    prog << CNOT(q[2], q[1])

    # H(1)
    prog << H(q[1])

    # Controlled-S dagger (control=1, target=0)
    csdg_gate = SDG(q[0]).control(q[1])
    prog << csdg_gate

    return prog
