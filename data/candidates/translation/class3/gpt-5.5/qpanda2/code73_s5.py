# EVAL_META: task_id=73, framework=qpanda2, class=3
import pyqpanda as pq
import atexit

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(64)
c = machine.cAlloc_many(64)

def x_measurement(circuit, qubit, clbit):
    target_qubit = q[qubit] if isinstance(qubit, int) else qubit
    target_clbit = c[clbit] if isinstance(clbit, int) else clbit
    circuit.insert(pq.H(target_qubit))
    circuit.insert(pq.Measure(target_qubit, target_clbit))

atexit.register(machine.finalize)
