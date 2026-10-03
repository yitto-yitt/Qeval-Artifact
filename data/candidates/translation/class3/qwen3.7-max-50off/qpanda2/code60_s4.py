# EVAL_META: task_id=60, framework=qpanda2, class=3
import pyqpanda

machine = pyqpanda.CPUQVM()
machine.init()
qubits = machine.qAlloc_many(2)

def create_cy_gate():
    circuit = pyqpanda.QCircuit()
    circuit << pyqpanda.Sdag(qubits[1])
    circuit << pyqpanda.CNOT(qubits[0], qubits[1])
    circuit << pyqpanda.S(qubits[1])
    return circuit

machine.finalize()
