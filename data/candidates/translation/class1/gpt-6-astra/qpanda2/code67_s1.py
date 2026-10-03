# EVAL_META: task_id=67, framework=qpanda2, class=1
from numpy import pi
import pyqpanda as pq


def chsh_circuit(alice, bob):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)

    program = pq.QProg()
    program << pq.H(qubits[0])
    program << pq.CNOT(qubits[0], qubits[1])
    program << pq.RY(qubits[0], 0 if alice == 0 else -pi / 2)
    program << pq.Measure(qubits[0], cbits[0])
    program << pq.RY(qubits[1], -pi / 4 if bob == 0 else pi / 4)
    program << pq.Measure(qubits[1], cbits[1])

    machine.directly_run(program)

    if not hasattr(chsh_circuit, "_machines"):
        chsh_circuit._machines = []
    chsh_circuit._machines.append(machine)
    return program
