# EVAL_META: task_id=84, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(lambda: machine.finalize())


def controlled_custom_unitary_circuit():
    circuit = pq.QCircuit()
    circuit << pq.U3(qubits[1], 0.3, 0.2, 0.1).control([qubits[0]])
    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
