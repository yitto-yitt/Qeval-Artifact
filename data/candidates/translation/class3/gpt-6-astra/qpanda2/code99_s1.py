# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def remove_unassigned_parameterized_gates(circuit):
    if not isinstance(circuit, (pq.QCircuit, pq.QProg)):
        raise TypeError("circuit must be a pyQPanda QCircuit or QProg")
    return pq.deep_copy(circuit)


machine.finalize()
