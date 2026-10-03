# EVAL_META: task_id=86, framework=qpanda, class=3
import pyqpanda3.core as pq

def collect_linear_blocks_with_and_without_limit():
    machine = pq.CPUQVM()
    for init_name in ("init_qvm", "init", "initialize"):
        init_method = getattr(machine, init_name, None)
        if init_method is not None:
            try:
                init_method()
            except TypeError:
                pass
            break

    if hasattr(machine, "qAlloc_many"):
        qubits = machine.qAlloc_many(5)
    elif hasattr(machine, "qalloc_many"):
        qubits = machine.qalloc_many(5)
    else:
        qubits = [machine.qAlloc() for _ in range(5)]

    h_gate = getattr(pq, "H")
    cx_gate = getattr(pq, "CNOT", None)
    if cx_gate is None:
        cx_gate = getattr(pq, "CX")

    def append(container, node):
        try:
            result = container << node
            return container if result is None else result
        except TypeError:
            result = container.insert(node)
            return container if result is None else result

    cx_chain = [(0, 1), (1, 2), (2, 3), (3, 4)]

    def linear_blocks(max_width=None):
        if max_width is None:
            return [cx_chain[:]]
        blocks = []
        current = []
        used = set()
        for control, target in cx_chain:
            new_used = used | {control, target}
            if current and len(new_used) > max_width:
                blocks.append(current)
                current = [(control, target)]
                used = {control, target}
            else:
                current.append((control, target))
                used = new_used
        if current:
            blocks.append(current)
        return blocks

    def build_program(max_width=None):
        prog = pq.QProg()
        prog = append(prog, h_gate(qubits[0]))
        for block in linear_blocks(max_width):
            circuit = pq.QCircuit()
            for control, target in block:
                circuit = append(circuit, cx_gate(qubits[control], qubits[target]))
            prog = append(prog, circuit)
        return prog

    full_block = build_program(None)
    limited_block = build_program(3)

    def execute(prog):
        for run_name in ("prob_run_dict", "prob_run_tuple_list"):
            run_method = getattr(machine, run_name, None)
            if run_method is not None:
                try:
                    return run_method(prog, qubits, -1)
                except TypeError:
                    try:
                        return run_method(prog, qubits)
                    except TypeError:
                        pass
        run_method = getattr(machine, "directly_run", None)
        if run_method is not None:
            try:
                return run_method(prog)
            except TypeError:
                pass
        run_method = getattr(machine, "run", None)
        if run_method is not None:
            try:
                return run_method(prog)
            except TypeError:
                pass
        return None

    execute(full_block)
    execute(limited_block)

    collect_linear_blocks_with_and_without_limit._machine = machine
    collect_linear_blocks_with_and_without_limit._qubits = qubits

    return full_block, limited_block
