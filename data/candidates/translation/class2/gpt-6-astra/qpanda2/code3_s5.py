# EVAL_META: task_id=3, framework=qpanda2, class=2
import pyqpanda as pq
from pyqpanda.Visualization import draw_qprog


def create_ghz(drawing=False):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)

    ghz = pq.QProg()
    ghz << pq.H(qubits[0])
    ghz << pq.CNOT(qubits[0], qubits[1])
    ghz << pq.CNOT(qubits[0], qubits[2])
    for qubit, cbit in zip(qubits, cbits):
        ghz << pq.Measure(qubit, cbit)

    machine.directly_run(ghz)

    if not hasattr(create_ghz, "_machines"):
        create_ghz._machines = []
    create_ghz._machines.append(machine)

    if drawing:
        return ghz, draw_qprog(ghz, output="pic")
    return ghz
