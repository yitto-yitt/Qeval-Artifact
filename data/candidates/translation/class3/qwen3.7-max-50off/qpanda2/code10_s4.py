# EVAL_META: task_id=10, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init()
q = machine.qAlloc_many(2)

def create_operator():
    circ = pq.QCircuit()
    circ << pq.CNOT(q[0], q[1])
    circ << pq.CNOT(q[1], q[0])
    circ << pq.CNOT(q[0], q[1])
    return circ

machine.finalize()
