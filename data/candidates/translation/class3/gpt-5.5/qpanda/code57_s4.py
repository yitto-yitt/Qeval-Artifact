# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import *

def create_swap_gate():
    circuit = QCircuit()
    try:
        circuit << CNOT(0, 1)
        circuit << CNOT(1, 0)
        circuit << CNOT(0, 1)
        return circuit
    except Exception:
        machine = CPUQVM()
        if hasattr(machine, "init_qvm"):
            machine.init_qvm()
        elif hasattr(machine, "init"):
            machine.init()

        if hasattr(machine, "qAlloc_many"):
            qubits = machine.qAlloc_many(2)
        elif hasattr(machine, "qalloc_many"):
            qubits = machine.qalloc_many(2)
        else:
            qubits = [machine.qAlloc(), machine.qAlloc()]

        circuit = QCircuit()
        circuit << CNOT(qubits[0], qubits[1])
        circuit << CNOT(qubits[1], qubits[0])
        circuit << CNOT(qubits[0], qubits[1])

        create_swap_gate._machine = machine
        create_swap_gate._qubits = qubits
        return circuit
