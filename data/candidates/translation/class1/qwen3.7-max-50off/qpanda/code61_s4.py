# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QProg, Qubit, CBit, Measure

def create_quantum_circuit_with_one_qubit_and_measure():
    q = Qubit()
    c = CBit()
    prog = QProg()
    prog << Measure(q, c)
    return prog
