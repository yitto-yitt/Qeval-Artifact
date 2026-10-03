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
        if qubit < 0:
            raise IndexError("Qubit index must be nonnegative")
        if qubit >= len(qubits):
            qubits.extend(machine.qAlloc_many(qubit + 1 - len(qubits)))
        qubit = qubits[qubit]

    if isinstance(clbit, int):
        if clbit < 0:
            raise IndexError("Classical bit index must be nonnegative")
        if clbit >= len(cbits):
            cbits.extend(machine.cAlloc_many(clbit + 1 - len(cbits)))
        clbit = cbits[clbit]

    circuit << pq.H(qubit)
    circuit << pq.Measure(qubit, clbit)
    machine.directly_run(circuit)
