# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def remove_unassigned_parameterized_gates(circuit):
    return circuit

machine.finalize()
