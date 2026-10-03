# EVAL_META: task_id=110, framework=qpanda2, class=3
import pyqpanda

machine = pyqpanda.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(20)
c = machine.cAlloc_many(20)

def equivalent_clifford_circuit(circuit, n):
    return [circuit for _ in range(n)]

machine.finalize()
