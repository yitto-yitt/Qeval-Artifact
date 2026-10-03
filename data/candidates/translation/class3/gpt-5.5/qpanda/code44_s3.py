# EVAL_META: task_id=44, framework=qpanda, class=3
import pyqpanda3.core as pq

def tensor_circuits():
    theta = 0.2
    tensored = pq.QCircuit()
    tensored << pq.X(0)
    tensored << pq.RY(2, theta / 2.0)
    tensored << pq.CNOT(1, 2)
    tensored << pq.RY(2, -theta / 2.0)
    tensored << pq.CNOT(1, 2)
    return tensored
