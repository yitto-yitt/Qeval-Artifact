# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import *
from math import pi

def create_ch_gate():
    machine = CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(2)
    else:
        qubits = machine.qalloc_many(2)

    circuit = QCircuit()
    cnot_gate = globals().get("CNOT", globals().get("CX"))

    for gate in (
        RY(qubits[1], pi / 4),
        cnot_gate(qubits[0], qubits[1]),
        RY(qubits[1], -pi / 4),
    ):
        if hasattr(circuit, "insert"):
            circuit.insert(gate)
        else:
            circuit << gate

    if not hasattr(create_ch_gate, "_machines"):
        create_ch_gate._machines = []
    create_ch_gate._machines.append(machine)

    return circuit
