# EVAL_META: task_id=36, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, QProg, CNOT

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)
atexit.register(lambda: machine.finalize())


def bv_function(s):
    n = len(s)
    while len(qubits) < n + 1:
        qubits.append(machine.qAlloc())

    circuit = QCircuit()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            circuit << CNOT(qubits[index], qubits[n])

    program = QProg()
    program << circuit
    machine.directly_run(program)
    return circuit
