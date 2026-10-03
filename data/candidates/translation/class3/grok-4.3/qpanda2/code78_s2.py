# EVAL_META: task_id=78, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)
def qft_no_swaps(num_qubits):
    q = qubits[:num_qubits]
    circuit = pq.QCircuit()
    for i in range(num_qubits - 1, -1, -1):
        circuit << pq.H(q[i])
        for j in range(i - 1, -1, -1):
            circuit << pq.CR(q[j], q[i], pq.pi / (2 ** (i - j)))
    return circuit.dagger()
machine.finalize()
