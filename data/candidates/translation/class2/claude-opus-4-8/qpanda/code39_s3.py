# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import QCircuit, QProg, H, QMachine

def create_uniform_superposition(n):
    circ = QCircuit(n)
    for i in range(n):
        circ << H(i)
    prog = QProg()
    prog << circ
    machine = QMachine()
    machine.run(prog)
    return machine.result().get_statevector()
