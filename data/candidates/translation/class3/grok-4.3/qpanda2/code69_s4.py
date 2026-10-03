# EVAL_META: task_id=69, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.initQVM()
q = machine.qAlloc_many(2)
def create_quantum_circuit_based_h0_cs01_h1_csdg10():
    circuit = QCircuit()
    circuit << H(q[0]) << S(q[1]).control(q[0]) << H(q[1]) << S(q[0]).dagger().control(q[1])
    return circuit
machine.finalize()
