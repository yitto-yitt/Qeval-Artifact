# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, Qubit, H

def create_controlled_hgate():
    q = Qubit(3)
    circuit = QCircuit()
    circuit << H(q[2]).control([q[0], q[1]])
    return circuit
