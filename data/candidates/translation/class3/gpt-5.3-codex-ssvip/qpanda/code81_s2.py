# EVAL_META: task_id=81, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, ClassicalCondition, H, CNOT

def convert_qasm_string_to_quantum_circuit():
    q0 = Qubit(0)
    q1 = Qubit(1)
    c0 = ClassicalCondition(0)
    c1 = ClassicalCondition(1)

    prog = QProg()
    prog.insert(H(q0))
    prog.insert(CNOT(q0, q1))
    return prog
