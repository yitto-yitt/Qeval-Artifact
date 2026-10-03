# EVAL_META: task_id=60, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init()
qubits = machine.qAlloc_many(2)

def create_cy_gate():
    cir = pq.QCircuit()
    cir.insert(pq.S(qubits[1]).dagger())
    cir.insert(pq.CNOT(qubits[0], qubits[1]))
    cir.insert(pq.S(qubits[1]))
    return cir

machine.finalize()
