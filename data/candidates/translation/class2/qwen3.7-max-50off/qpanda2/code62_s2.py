# EVAL_META: task_id=62, framework=qpanda2, class=2
import pyqpanda as pq

def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(num_qubits)
    circ = pq.QCircuit()
    for i in range(len(basis)):
        if state[i] == 1:
            circ << pq.X(qubits[i])
        if basis[i] == 1:
            circ << pq.H(qubits[i])
    return circ
