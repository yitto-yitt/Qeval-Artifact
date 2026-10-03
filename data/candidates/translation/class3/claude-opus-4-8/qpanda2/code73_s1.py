# EVAL_META: task_id=73, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)
cbits = machine.cAlloc_many(4)


def x_measurement(circuit, qubit, clbit):
    circuit << H(qubits[qubit])
    circuit << Measure(qubits[qubit], cbits[clbit])
    return circuit


if __name__ == "__main__":
    prog = QProg()
    x_measurement(prog, 0, 0)
    result = machine.run_with_configuration(prog, [cbits[0]], 1000)
    print(result)
    machine.finalize()
