# EVAL_META: task_id=109, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def circuit():
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    theta = pq.Parameter('th')
    prog.insert(pq.RZ(qubits[0], theta))
    return prog, qubits

prog, qubits = circuit()
machine.finalize()
