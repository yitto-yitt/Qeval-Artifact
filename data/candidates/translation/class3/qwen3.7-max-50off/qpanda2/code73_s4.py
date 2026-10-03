# EVAL_META: task_id=73, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(10)
c = machine.cAlloc_many(10)

def x_measurement(circuit, qubit, clbit):
    circuit.insert(pq.H(qubit))
    circuit.insert(pq.Measure(qubit, clbit))
    return circuit

machine.finalize()
