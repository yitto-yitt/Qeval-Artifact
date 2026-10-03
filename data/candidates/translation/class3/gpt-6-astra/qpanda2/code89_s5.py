# EVAL_META: task_id=89, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_controlled_hgate():
    circuit = pq.QCircuit()
    circuit << pq.H(qubits[2]).control([qubits[0], qubits[1]])
    program = pq.QProg()
    program << circuit
    machine.directly_run(program)
    return circuit

atexit.register(lambda: machine.finalize())
