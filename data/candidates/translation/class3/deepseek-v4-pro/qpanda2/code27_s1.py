# EVAL_META: task_id=27, framework=qpanda2, class=3
from pyqpanda import CPUQVM, QProg, H, CNOT, DAGCircuit

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def apply_op_back():
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    dag = DAGCircuit()
    dag.build_dag_circuit(prog, machine)

    if hasattr(dag, "apply_operation_back"):
        dag.apply_operation_back(H(q[0]))
        return dag

    prog2 = QProg()
    prog2 << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    dag2 = DAGCircuit()
    dag2.build_dag_circuit(prog2, machine)
    return dag2

machine.finalize()
