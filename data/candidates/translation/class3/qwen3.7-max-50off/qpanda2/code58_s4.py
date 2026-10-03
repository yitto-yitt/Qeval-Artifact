# EVAL_META: task_id=58, framework=qpanda2, class=3
import pyqpanda as pq
from numpy import pi

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_ch_gate():
    circuit = pq.QCircuit()
    circuit << pq.RY(q[1], pi/4)
    circuit << pq.CNOT(q[0], q[1])
    circuit << pq.RY(q[1], -pi/4)
    return circuit

machine.finalize()
