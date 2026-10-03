# EVAL_META: task_id=73, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_q = machine.qAlloc_many(64)
_c = machine.cAlloc_many(64)

def x_measurement(circuit, qubit, clbit):
    circuit.insert(pq.H(_q[qubit]))
    circuit.insert(pq.Measure(_q[qubit], _c[clbit]))
    return circuit

machine.finalize()
