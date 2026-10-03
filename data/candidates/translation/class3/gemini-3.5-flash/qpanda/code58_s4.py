# EVAL_META: task_id=58, framework=qpanda, class=3
import pyqpanda3.core as pq
from numpy import pi

def create_ch_gate():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    circuit = pq.QCircuit()
    circuit << pq.RY(q[1], pi/4) << pq.CNOT(q[0], q[1]) << pq.RY(q[1], -pi/4)
    return circuit
