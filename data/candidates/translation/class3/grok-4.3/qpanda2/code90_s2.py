# EVAL_META: task_id=90, framework=qpanda2, class=3
import pyqpanda as pq
machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)
def create_custom_controlled():
    prog = pq.QProg()
    custom = pq.QCircuit()
    custom << pq.X(qubits[1]) << pq.H(qubits[2])
    controlled_custom = custom.control([qubits[0], qubits[3]])
    prog << controlled_custom
    return prog
machine.finalize()
