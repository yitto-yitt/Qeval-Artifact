# EVAL_META: task_id=125, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(64)


def circ_to_gate(circ):
    circ_gate = pq.QCircuit()
    circ_gate.insert(circ)
    return circ_gate


machine.finalize()
