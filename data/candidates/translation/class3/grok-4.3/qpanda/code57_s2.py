# EVAL_META: task_id=57, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_swap_gate():
    circuit = pq.QCircuit()
    q = [pq.Qubit(i) for i in range(2)]
    circuit << pq.CNOT(q[0], q[1])
    circuit << pq.CNOT(q[1], q[0])
    circuit << pq.CNOT(q[0], q[1])
    return circuit
