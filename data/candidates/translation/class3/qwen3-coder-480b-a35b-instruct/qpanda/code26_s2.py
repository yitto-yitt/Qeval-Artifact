# EVAL_META: task_id=26, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit, H, CNOT, Measure


def bell_dag():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = [machine.qAlloc() for _ in range(3)]
    c = [machine.cAlloc() for _ in range(3)]
    
    prog = QProg()
    prog.insert(H(q[0]))
    prog.insert(CNOT(q[0], q[1]))
    prog.insert(Measure(q[0], c[0]))
    
    # In pyQPanda3, we don't have a direct DAG representation like Qiskit
    # Instead, we return the quantum program which represents the circuit structure
    return prog
