# EVAL_META: task_id=125, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QCircuit, QProg

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)


def circ_to_gate(circ):
    if isinstance(circ, QProg):
        gate = QCircuit()
        for node in circ:
            gate.insert(node)
        return gate
    elif isinstance(circ, QCircuit):
        gate = QCircuit()
        gate.insert(circ)
        return gate
    else:
        gate = QCircuit()
        gate.insert(circ)
        return gate


machine.finalize()
