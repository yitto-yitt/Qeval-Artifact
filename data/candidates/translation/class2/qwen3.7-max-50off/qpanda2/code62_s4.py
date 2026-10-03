# EVAL_META: task_id=62, framework=qpanda2, class=2
import pyqpanda as pq

def bb84_senders_circuit(state, basis):
    num_qubits = len(state)
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qAlloc_many(num_qubits)
    circ = pq.QCircuit()
    for i in range(len(basis)):
        if state[i] == 1:
            circ << pq.X(q[i])
        if basis[i] == 1:
            circ << pq.H(q[i])
    return circ
