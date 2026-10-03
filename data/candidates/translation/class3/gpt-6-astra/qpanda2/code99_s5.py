# EVAL_META: task_id=99, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def remove_unassigned_parameterized_gates(circuit):
    # Native pyQPanda gates accept only bound numerical parameters.
    # Consequently, every gate in a native circuit must be retained.
    if isinstance(circuit, pq.QCircuit):
        return pq.QCircuit(circuit)
    if isinstance(circuit, pq.QProg):
        return pq.QProg(circuit)
    raise TypeError("circuit must be a pyqpanda.QCircuit or pyqpanda.QProg")


machine.finalize()
