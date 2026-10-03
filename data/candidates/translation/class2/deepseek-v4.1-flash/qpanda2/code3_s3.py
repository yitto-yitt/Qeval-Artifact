# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import QCircuit, QProg, Qubit, CBit, H, CNOT, measure


def create_ghz(drawing=False):
    q0, q1, q2 = Qubit(0), Qubit(1), Qubit(2)
    c0, c1, c2 = CBit(0), CBit(1), CBit(2)

    circuit = QCircuit()
    circuit << H(q0)
    circuit << CNOT(q0, q1)
    circuit << CNOT(q0, q2)

    prog = QProg()
    prog << circuit
    prog << measure(q0, c0)
    prog << measure(q1, c1)
    prog << measure(q2, c2)

    if drawing:
        from pyqpanda.utils import draw_qprog
        return prog, draw_qprog(prog, 'pic')

    return prog

