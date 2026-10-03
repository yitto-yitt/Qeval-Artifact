# EVAL_META: task_id=130, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
MAX_QUBITS = 64
q = machine.qAlloc_many(MAX_QUBITS)

def inv_circuit(n):
    prog = pq.QProg()
    for i in range(2):
        prog.insert(pq.H(q[i + 1]))
    for i in range(2):
        prog.insert(pq.CNOT(q[i + 1], q[i + 3]))
    inv_prog = pq.get_inverse_qprog(prog)
    machine.finalize()
    return inv_prog
