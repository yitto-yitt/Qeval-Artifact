# EVAL_META: task_id=71, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def create_quantum_circuit_based_h0_csx01_h1():
    circuit = pq.QCircuit()
    circuit << pq.H(qubits[0])
    circuit << pq.H(qubits[1])
    circuit << pq.S(qubits[1]).control([qubits[0]])
    circuit << pq.H(qubits[1])
    circuit << pq.H(qubits[1])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit


atexit.register(lambda: machine.finalize())
