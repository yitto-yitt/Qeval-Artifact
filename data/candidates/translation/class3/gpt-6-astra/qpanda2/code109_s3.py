# EVAL_META: task_id=109, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)

def circuit():
    th = pq.var(0.0, True)
    qc = pq.VariationalQuantumCircuit()
    qc.insert(pq.VariationalQuantumGate_H(qubits[0]))
    qc.insert(pq.VariationalQuantumGate_RZ(qubits[0], th))

    program = pq.QProg()
    program.insert(qc.feed())
    machine.directly_run(program)
    return qc

atexit.register(machine.finalize)
