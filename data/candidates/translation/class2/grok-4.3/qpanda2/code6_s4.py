# EVAL_META: task_id=6, framework=qpanda2, class=2
import pyqpanda as pq


def create_state_prep(num_qubits):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qlist = qvm.qAlloc_many(num_qubits)
    circuit = pq.QCircuit()
    circuit << pq.X(qlist[0])
    return circuit
