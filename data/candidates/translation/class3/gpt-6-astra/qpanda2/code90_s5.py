# EVAL_META: task_id=90, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_custom_controlled():
    custom = pq.QCircuit()
    custom << pq.X(qubits[1])
    custom << pq.H(qubits[2])
    controlled = custom.control([qubits[0], qubits[3]])

    program = pq.QProg()
    program << controlled
    machine.directly_run(program)
    return program

atexit.register(lambda: machine.finalize())
