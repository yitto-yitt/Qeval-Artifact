# EVAL_META: task_id=70, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
atexit.register(lambda: machine.finalize())


def create_quantum_circuit_based_h0_cswap012_h1_csdg10():
    circuit = pq.QCircuit()
    circuit << pq.H(qubits[0])
    circuit << pq.SWAP(qubits[1], qubits[2]).control([qubits[0]])
    circuit << pq.H(qubits[1])
    circuit << pq.S(qubits[0]).dagger().control([qubits[1]])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
