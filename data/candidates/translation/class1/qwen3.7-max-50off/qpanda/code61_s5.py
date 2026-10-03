# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, Measure

def create_quantum_circuit_with_one_qubit_and_measure():
    qm = QuantumMachine()
    q = qm.qAlloc(1)
    c = qm.cAlloc(1)
    prog = QProg()
    prog << Measure(q[0], c[0])
    return prog
