# EVAL_META: task_id=73, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
clbits = machine.cAlloc_many(1)
atexit.register(lambda: machine.finalize())


def x_measurement(circuit, qubit, clbit):
    target = qubits[qubit] if isinstance(qubit, int) else qubit
    result = clbits[clbit] if isinstance(clbit, int) else clbit
    circuit.insert(pq.H(target))
    circuit.insert(pq.Measure(target, result))
