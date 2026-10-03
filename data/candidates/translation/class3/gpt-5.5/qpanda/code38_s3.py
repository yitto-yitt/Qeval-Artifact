# EVAL_META: task_id=38, framework=qpanda, class=3
import pyqpanda3.core as pq

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    machine = pq.CPUQVM()
    if hasattr(machine, "init_qvm"):
        machine.init_qvm()
    elif hasattr(machine, "init"):
        machine.init()

    q = machine.qAlloc_many(2)
    prog = pq.QProg()

    def controlled(gate, controls):
        try:
            result = gate.control(controls)
        except TypeError:
            result = gate.control(controls[0])
        return gate if result is None else result

    def append_op(program, op):
        try:
            return program << op
        except Exception:
            program.insert(op)
            return program

    prog = append_op(prog, pq.H(q[0]))
    prog = append_op(prog, controlled(pq.RZ(q[1], theta), [q[0]]))
    prog = append_op(prog, pq.H(q[1]))
    prog = append_op(prog, controlled(pq.RY(q[0], theta), [q[1]]))

    if not hasattr(create_quantum_circuit_based_h0_crz01_h1_cry10, "_machines"):
        create_quantum_circuit_based_h0_crz01_h1_cry10._machines = []
    create_quantum_circuit_based_h0_crz01_h1_cry10._machines.append(machine)

    return prog
