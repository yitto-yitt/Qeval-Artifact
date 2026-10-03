# EVAL_META: task_id=26, framework=qpanda2, class=3
import pyqpanda
from pyqpanda import CPUQVM, QProg, H, CNOT, Measure

qvm = CPUQVM()
qvm.init_qvm()
qubits = qvm.qAlloc_many(3)
cbits = qvm.cAlloc_many(3)

def bell_dag():
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << Measure(qubits[0], cbits[0])

    if hasattr(pyqpanda, 'get_dag'):
        try:
            return pyqpanda.get_dag(prog, qvm, cbits)
        except TypeError:
            return pyqpanda.get_dag(prog, qvm)

    if hasattr(pyqpanda, 'transform_qprog_to_dag'):
        try:
            return pyqpanda.transform_qprog_to_dag(prog, qvm, cbits)
        except TypeError:
            return pyqpanda.transform_qprog_to_dag(prog, qvm)

    if hasattr(pyqpanda, 'QProgToDAG'):
        try:
            return pyqpanda.QProgToDAG.get_dag(prog, qvm, cbits)
        except TypeError:
            return pyqpanda.QProgToDAG.get_dag(prog, qvm)

    raise ImportError("No DAG transformer found in pyqpanda")

qvm.finalize()
