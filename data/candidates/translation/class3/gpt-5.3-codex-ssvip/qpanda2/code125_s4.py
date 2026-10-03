# EVAL_META: task_id=125, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(1)

def circ_to_gate(circ):
    return circ

machine.finalize()
