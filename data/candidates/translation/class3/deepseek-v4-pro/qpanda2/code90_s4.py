# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, X, H

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)

def create_custom_controlled():
    circuit = QCircuit()
    circuit.insert(X(q[1]).control([q[0], q[3]]))
    circuit.insert(H(q[2]).control([q[0], q[3]]))
    return circuit

machine.finalize()
