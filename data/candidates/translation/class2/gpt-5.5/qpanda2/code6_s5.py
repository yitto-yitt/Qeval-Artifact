# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)

    circuit = pq.QCircuit()
    if num_qubits > 0:
        circuit.insert(pq.X(qubits[0]))

    if not hasattr(create_state_prep, "_resources"):
        create_state_prep._resources = []
    create_state_prep._resources.append((qvm, qubits))

    return circuit
