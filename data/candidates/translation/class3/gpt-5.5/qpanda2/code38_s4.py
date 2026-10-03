# EVAL_META: task_id=38, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, H, RZ, RY

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    circuit = QCircuit()
    circuit.insert(H(q[0]))
    circuit.insert(RZ(q[1], theta).control([q[0]]))
    circuit.insert(H(q[1]))
    circuit.insert(RY(q[0], theta).control([q[1]]))
    return circuit

atexit.register(machine.finalize)
