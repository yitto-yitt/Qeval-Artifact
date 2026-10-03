# EVAL_META: task_id=26, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)
cbits = machine.cAlloc_many(3)


def bell_dag():
    try:
        program = pq.QProg()
        program << pq.H(qubits[0])
        program << pq.CNOT(qubits[0], qubits[1])
        program << pq.Measure(qubits[0], cbits[0])

        machine.directly_run(program)

        converter = getattr(pq, "convert_qprog_to_dag", None)
        if converter is not None:
            return converter(program)

        dag_type = getattr(pq, "QProgDAG", None)
        if dag_type is not None:
            try:
                return dag_type(program)
            except TypeError:
                dag = dag_type()
                builder = getattr(dag, "build_dag", None)
                if builder is not None:
                    builder(program)
                    return dag

        return pq.circuit_layer(program)
    finally:
        machine.finalize()
