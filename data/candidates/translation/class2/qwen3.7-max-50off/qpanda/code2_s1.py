# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import QProg, H, CNOT, qalloc, StateVectorSimulator

def create_bell_statevector():
    q = qalloc(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    sim = StateVectorSimulator()
    sim.init_qubits(2)
    sim.run(prog)
    return sim.get_statevector()
