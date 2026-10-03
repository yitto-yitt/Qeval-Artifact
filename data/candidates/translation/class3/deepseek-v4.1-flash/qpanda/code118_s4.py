# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, qubit, SX

def create_c3sx_circuit():
    q = qubit(4)
    circuit = QCircuit()
    circuit << SX(q[3]).control([q[0], q[1], q[2]])
    return circuit
