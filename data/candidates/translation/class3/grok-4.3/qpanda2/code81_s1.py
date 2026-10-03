# EVAL_META: task_id=81, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)
def convert_qasm_string_to_quantum_circuit():
    circuit = QCircuit()
    circuit << H(q[0]) << CNOT(q[0], q[1])
    return circuit
machine.finalize()
