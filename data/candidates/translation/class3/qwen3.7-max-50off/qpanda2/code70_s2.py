# EVAL_META: task_id=70, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init()
q = machine.qAlloc_many(3)

def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circ = pq.QCircuit()
    circ << pq.H(q[0])
    circ << pq.Fredkin(q[0], q[1], q[2])
    circ << pq.H(q[1])
    circ << pq.Sdag(q[0]).control(q[1])
    return circ

machine.finalize()
