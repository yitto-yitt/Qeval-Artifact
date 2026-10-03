# EVAL_META: task_id=110, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
cbits = machine.cAlloc_many(20)

def equivalent_clifford_circuit(circuit, n):
    return [circuit for _ in range(n)]

machine.finalize()
