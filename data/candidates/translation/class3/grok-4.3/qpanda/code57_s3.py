# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import init_quantum_machine, QuantumMachineType, QCircuit, CNOT

def create_swap_gate():
    machine = init_quantum_machine(QuantumMachineType.CPU_SINGLE_THREAD)
    qubits = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit << CNOT(qubits[0], qubits[1])
    circuit << CNOT(qubits[1], qubits[0])
    circuit << CNOT(qubits[0], qubits[1])
    return circuit
