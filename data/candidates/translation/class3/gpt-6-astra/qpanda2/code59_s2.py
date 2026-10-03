# EVAL_META: task_id=59, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_cz_gate():
    circuit = pq.QCircuit()
    circuit << pq.H(qubits[1])
    circuit << pq.CNOT(qubits[0], qubits[1])
    circuit << pq.H(qubits[1])

    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit

atexit.register(machine.finalize)
