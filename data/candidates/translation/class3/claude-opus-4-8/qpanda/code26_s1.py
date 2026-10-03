# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, CNOT, measure


def bell_dag():
    qubits = list(range(3))
    cbits = list(range(3))
    circ = QCircuit()
    circ << H(qubits[0])
    circ << CNOT(qubits[0], qubits[1])
    prog = QProg()
    prog << circ
    prog << measure(qubits[0], cbits[0])
    dag = prog.to_dag()
    return dag
