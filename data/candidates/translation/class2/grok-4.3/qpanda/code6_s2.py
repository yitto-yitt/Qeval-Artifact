# EVAL_META: task_id=6, framework=qpanda, class=2
import pyqpanda3.core as pq


def create_state_prep(num_qubits):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    qc = pq.QCircuit()
    qc.insert(pq.X(qubits[0]))
    return qc
