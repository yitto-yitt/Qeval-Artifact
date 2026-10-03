# EVAL_META: task_id=39, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit, init_cpu_quantum_machine

def create_uniform_superposition(n):
    qvm = init_cpu_quantum_machine()
    qvm.qAlloc_many(n)
    circ = QuantumCircuit(n)
    for i in range(n):
        circ.h(i)
    qvm.run(circ)
    return qvm.get_state()
