# EVAL_META: task_id=27, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, QProgToDAG


def apply_op_back():
    qvm = CPUQVM()
    qvm.initQVM()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])

    try:
        dag_builder = QProgToDAG(prog)
    except TypeError:
        dag_builder = QProgToDAG()
        dag_builder.transform(prog)

    if hasattr(dag_builder, "getDAGCircuit"):
        dag = dag_builder.getDAGCircuit()
    elif hasattr(dag_builder, "get_dag_circuit"):
        dag = dag_builder.get_dag_circuit()
    else:
        dag = dag_builder

    try:
        dag.add_qgate(H(q[0]))
    except (AttributeError, TypeError):
        prog << H(q[0])
        try:
            dag_builder = QProgToDAG(prog)
        except TypeError:
            dag_builder = QProgToDAG()
            dag_builder.transform(prog)

        if hasattr(dag_builder, "getDAGCircuit"):
            dag = dag_builder.getDAGCircuit()
        elif hasattr(dag_builder, "get_dag_circuit"):
            dag = dag_builder.get_dag_circuit()
        else:
            dag = dag_builder

    return dag
