# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import CPUQVM, QProg, H, CNOT, Measure, draw_qprog


def create_ghz(drawing=False):
    if not hasattr(create_ghz, "_resources"):
        machine = CPUQVM()
        machine.init_qvm()
        qubits = machine.qAlloc_many(3)
        cbits = machine.cAlloc_many(3)
        create_ghz._resources = machine, qubits, cbits

    machine, qubits, cbits = create_ghz._resources
    ghz = QProg()
    ghz << H(qubits[0])
    ghz << CNOT(qubits[0], qubits[1])
    ghz << CNOT(qubits[0], qubits[2])
    for qubit, cbit in zip(qubits, cbits):
        ghz << Measure(qubit, cbit)

    machine.run_with_configuration(ghz, cbits, 1)

    if drawing:
        return ghz, draw_qprog(ghz, output="pic")
    return ghz
