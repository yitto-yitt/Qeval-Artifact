# EVAL_META: task_id=44, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def tensor_circuits():
    bottom = pq.QCircuit()
    bottom << pq.RY(qubits[1], 0.2).control([qubits[0]])

    top = pq.QCircuit()
    top << pq.X(qubits[2])

    tensored = pq.QCircuit()
    tensored << bottom << top
    return tensored

atexit.register(machine.finalize)
