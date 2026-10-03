# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QuantumEnvironment, QProg, H, CNOT, Measure

def bell_dag():
    env = QuantumEnvironment()
    q = env.alloc_qubits(3)
    c = env.alloc_cbits(3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    return prog
