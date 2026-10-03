# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import init_quantum_machine, QuantumMachineType, QProg, H, CNOT, Measure, circuit_to_dag


def bell_dag():
    qvm = init_quantum_machine(QuantumMachineType.CPU)
    q = qvm.allocate_qubits(3)
    c = qvm.allocate_cbits(3)
    circ = QProg()
    circ << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    dag = circuit_to_dag(circ)
    return dag
