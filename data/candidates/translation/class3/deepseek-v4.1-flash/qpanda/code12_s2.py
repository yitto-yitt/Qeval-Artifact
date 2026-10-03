# EVAL_META: task_id=12, framework=qpanda, class=3
import pyqpanda3.core as pq

def get_unitary():
    circ = pq.QCircuit()
    q0 = pq.Qubit(0)
    q1 = pq.Qubit(1)
    circ << pq.H(q1) << pq.CNOT(q1, q0)
    return pq.get_unitary(circ)
