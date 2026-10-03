# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import ClassicalRegister, QuantumCircuit, QuantumRegister
from pyqpanda3.core import HGate
from pyqpanda3.core import circuit_to_dag


def apply_op_back():
    q = QuantumRegister(3, "q")
    c = ClassicalRegister(3, "c")
    circ = QuantumCircuit(q, c)
    circ.h(q[0])
    circ.cx(q[0], q[1])
    dag = circuit_to_dag(circ)
    dag.apply_operation_back(HGate(), qargs=[q[0]])
    return dag
