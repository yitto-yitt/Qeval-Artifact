# EVAL_META: task_id=14, framework=qpanda, class=1
import pyqpanda3.core as pq

def bell_each_shot():
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.measure_all(q, c)
    result = machine.run_with_configuration(prog, c, 10)
    total = sum(result.values())
    probs = {key: value / total for key, value in result.items()}
    machine.finalize()
    return probs
