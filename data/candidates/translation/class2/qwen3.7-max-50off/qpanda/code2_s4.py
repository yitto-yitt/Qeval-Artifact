# EVAL_META: task_id=2, framework=qpanda, class=2
from pyqpanda3.core import QuantumMachine, QuantumCircuit

def create_bell_statevector():
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    circ = QuantumCircuit()
    circ.h(q[0])
    circ.cnot(q[0], q[1])
    qm.run(circ)
    return qm.get_state()
