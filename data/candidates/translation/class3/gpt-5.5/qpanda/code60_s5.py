# EVAL_META: task_id=60, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_cy_gate():
    circuit = pq.QCircuit()
    circuit << pq.S(1).dagger()
    circuit << pq.CNOT(0, 1)
    circuit << pq.S(1)
    return circuit
