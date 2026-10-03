# EVAL_META: task_id=71, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, H, X

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)


def create_quantum_circuit_based_h0_csx01_h1():
    circuit = QCircuit()
    circuit << H(qubits[0])
    sx = X(qubits[1]).control([qubits[0]])
    csx = QCircuit()
    csx << H(qubits[1]).control([qubits[0]])
    csx << X(qubits[1]).control([qubits[0]])
    csx << H(qubits[1]).control([qubits[0]])
    circuit << csx
    circuit << H(qubits[1])
    return circuit


if __name__ == "__main__":
    prog = create_quantum_circuit_based_h0_csx01_h1()
    machine.finalize()
