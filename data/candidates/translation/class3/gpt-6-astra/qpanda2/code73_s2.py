# EVAL_META: task_id=73, framework=qpanda2, class=3
import atexit
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
cbits = machine.cAlloc_many(1)
atexit.register(machine.finalize)


def x_measurement(circuit, qubit, clbit):
    if isinstance(qubit, int):
        while len(qubits) <= qubit:
            qubits.append(machine.qAlloc())
        qubit = qubits[qubit]
    if isinstance(clbit, int):
        while len(cbits) <= clbit:
            cbits.append(machine.cAlloc())
        clbit = cbits[clbit]
    circuit << pq.H(qubit)
    circuit << pq.Measure(qubit, clbit)
    machine.directly_run(circuit)
