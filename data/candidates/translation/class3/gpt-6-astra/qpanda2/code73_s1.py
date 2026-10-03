# EVAL_META: task_id=73, framework=qpanda2, class=3
import atexit
from numbers import Integral
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
cbits = machine.cAlloc_many(1)
atexit.register(machine.finalize)


def x_measurement(circuit, qubit, clbit):
    if isinstance(qubit, Integral):
        index = int(qubit)
        if index < 0:
            raise IndexError("qubit index must be nonnegative")
        if index >= len(qubits):
            qubits.extend(machine.qAlloc_many(index + 1 - len(qubits)))
        qubit = qubits[index]

    if isinstance(clbit, Integral):
        index = int(clbit)
        if index < 0:
            raise IndexError("classical bit index must be nonnegative")
        if index >= len(cbits):
            cbits.extend(machine.cAlloc_many(index + 1 - len(cbits)))
        clbit = cbits[index]

    circuit << pq.H(qubit)
    circuit << pq.Measure(qubit, clbit)
    machine.directly_run(circuit)
