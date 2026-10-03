# EVAL_META: task_id=69, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg, H, S

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
_circuit = None


def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    global _circuit
    if _circuit is None:
        circuit = QCircuit()
        circuit << H(qubits[0])
        circuit << S(qubits[1]).control([qubits[0]])
        circuit << H(qubits[1])
        circuit << S(qubits[0]).dagger().control([qubits[1]])

        program = QProg()
        program << circuit
        machine.directly_run(program)
        _circuit = circuit
    return _circuit


try:
    create_quantum_circuit_based_h0_cs01_h1_csdg10()
finally:
    machine.finalize()
