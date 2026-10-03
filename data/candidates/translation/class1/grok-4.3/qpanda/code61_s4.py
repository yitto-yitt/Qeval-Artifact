# EVAL_META: task_id=61, framework=qpanda, class=1
from pyqpanda3.core import init_quantum_machine, QMachineType, QCircuit, measure

def create_quantum_circuit_with_one_qubit_and_measure():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    qc = QCircuit()
    qc << measure(q[0], c[0])
    return qc
