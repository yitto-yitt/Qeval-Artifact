# EVAL_META: task_id=10, framework=qpanda2, class=3
import atexit
import math
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)


def create_operator():
    circuit = pq.QCircuit()
    circuit << pq.U3(qubits[0], math.pi, 0.0, math.pi)
    circuit << pq.U3(qubits[1], math.pi, 0.0, math.pi)

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(lambda: machine.finalize())
