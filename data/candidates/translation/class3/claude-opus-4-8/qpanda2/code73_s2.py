# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)
cbits = machine.cAlloc_many(4)


def x_measurement(circuit, qubit, clbit):
    circuit << H(qubit)
    circuit << Measure(qubit, clbit)
    return circuit


if __name__ == "__main__":
    prog = QProg()
    x_measurement(prog, qubits[0], cbits[0])
    result = machine.run_with_configuration(prog, cbits, 1024)
    print(result)
    machine.finalize()
