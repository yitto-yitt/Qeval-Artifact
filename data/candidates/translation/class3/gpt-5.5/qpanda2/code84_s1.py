# EVAL_META: task_id=84, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def controlled_custom_unitary_circuit():
    circuit = pq.QCircuit()
    circuit.insert(pq.U3(qubits[1], 0.3, 0.2, 0.1).control([qubits[0]]))
    return circuit

atexit.register(machine.finalize)
