# EVAL_META: task_id=10, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_operator():
    circuit = pq.QCircuit()
    circuit << pq.X(qubits[0]) << pq.X(qubits[1])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(machine.finalize)
