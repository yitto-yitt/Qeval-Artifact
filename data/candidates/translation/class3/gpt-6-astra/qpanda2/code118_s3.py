# EVAL_META: task_id=118, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)


def create_c3sx_circuit():
    circuit = pq.QCircuit()
    circuit << pq.H(qubits[3])
    circuit << pq.S(qubits[3]).control(qubits[:3])
    circuit << pq.H(qubits[3])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(machine.finalize)
