# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import QProg, allocate_qubits, allocate_classical_bits, H, CNOT, qprog_to_dag, DAGNode

def apply_op_back():
    q = allocate_qubits(3)
    c = allocate_classical_bits(3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    dag = qprog_to_dag(prog)
    dag.push_back_node(DAGNode(H(q[0])))
    return dag
