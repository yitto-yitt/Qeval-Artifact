# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda import *
from pyqpanda.core import *


def bell_dag():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(3)
    cbits = qvm.cAlloc_many(3)
    
    prog = QProg()
    prog.insert(single_gate_apply_to_all(H, qubits))
    prog.insert(CNOT(qubits[0], qubits[1]))
    prog.insert(Measure(qubits[0], cbits[0]))
    
    dag = prog.to_dag()
    return dag
