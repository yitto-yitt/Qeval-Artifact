# EVAL_META: task_id=89, framework=qpanda, class=3
from pyqpanda3.core import CPU, init_quantum_machine, QCircuit, H

def create_controlled_hgate():
    qvm = init_quantum_machine(CPU)
    q = qvm.qAlloc_many(3)
    circuit = QCircuit()
    gate = H(q[2]).control([q[0], q[1]])
    circuit << gate
    return circuit
