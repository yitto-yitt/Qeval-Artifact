# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import QuantumCircuit, AllocateQubits, AllocateCBits, H, CX, Measure
try:
    from pyqpanda3.core import draw_circuit
except ImportError:
    from pyqpanda3.core import draw_qprog as draw_circuit


def create_ghz(drawing=False):
    qubits = AllocateQubits(3)
    cbits = AllocateCBits(3)

    circuit = QuantumCircuit()
    circuit << H(qubits[0])
    circuit << CX(qubits[0], qubits[1])
    circuit << CX(qubits[0], qubits[2])
    circuit << Measure(qubits[0], cbits[0])
    circuit << Measure(qubits[1], cbits[1])
    circuit << Measure(qubits[2], cbits[2])

    if drawing:
        return circuit, draw_circuit(circuit)
    return circuit
