# EVAL_META: task_id=60, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_cy_gate():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    circuit = pq.QCircuit()
    circuit << pq.Sdg(q[1]) << pq.CNOT(q[0], q[1]) << pq.S(q[1])
    return circuit
