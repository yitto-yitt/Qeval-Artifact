# EVAL_META: task_id=130, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_q = machine.qAlloc_many(64)

def inv_circuit(n):
    qubits = _q[:n]
    prog = pq.QProg()
    circ = pq.QCircuit()
    for i in range(2):
        circ.insert(pq.H(qubits[i + 1]))
    for i in range(2):
        circ.insert(pq.CNOT(qubits[i + 1], qubits[i + 3]))
    prog.insert(circ.dagger())
    return prog

machine.finalize()
