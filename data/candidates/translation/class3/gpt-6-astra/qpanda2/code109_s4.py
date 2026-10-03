# EVAL_META: task_id=109, framework=qpanda2, class=3
import atexit
from pyqpanda import (
    CPUQVM,
    QProg,
    VariationalQuantumCircuit,
    VariationalQuantumGate_H,
    VariationalQuantumGate_RZ,
    var,
)

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(1)


def circuit():
    theta = var(0.0, True)
    qc = VariationalQuantumCircuit()
    qc.insert(VariationalQuantumGate_H(qubits[0]))
    qc.insert(VariationalQuantumGate_RZ(qubits[0], theta))

    program = QProg()
    program.insert(qc.eval())
    machine.directly_run(program)
    return qc


atexit.register(lambda: machine.finalize())
