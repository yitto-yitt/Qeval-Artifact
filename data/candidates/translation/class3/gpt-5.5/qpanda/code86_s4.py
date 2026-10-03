# EVAL_META: task_id=86, framework=qpanda, class=3
import pyqpanda3.core as pq

def collect_linear_blocks_with_and_without_limit():
    cnot_gate = getattr(pq, "CNOT", None)
    if cnot_gate is None:
        cnot_gate = getattr(pq, "CX")

    def new_top():
        cls = getattr(pq, "QProg", None)
        if cls is None:
            cls = getattr(pq, "QCircuit")
        try:
            return cls()
        except TypeError:
            return cls(5)

    def new_block():
        cls = getattr(pq, "QCircuit", None)
        if cls is None:
            cls = getattr(pq, "QProg")
        try:
            return cls()
        except TypeError:
            return cls(5)

    def append(container, item):
        try:
            container << item
            return container
        except Exception as first_error:
            if hasattr(container, "insert"):
                try:
                    container.insert(item)
                    return container
                except Exception:
                    pass
            if hasattr(container, "append"):
                try:
                    container.append(item)
                    return container
                except Exception:
                    pass
            raise first_error

    machine = None
    try:
        pq.H(0)
        cnot_gate(0, 1)
        qubits = list(range(5))
    except Exception:
        machine = pq.CPUQVM()
        if hasattr(machine, "init_qvm"):
            machine.init_qvm()
        elif hasattr(machine, "initQVM"):
            machine.initQVM()
        if hasattr(machine, "qAlloc_many"):
            qubits = machine.qAlloc_many(5)
        elif hasattr(machine, "qalloc_many"):
            qubits = machine.qalloc_many(5)
        elif hasattr(machine, "qAllocMany"):
            qubits = machine.qAllocMany(5)
        else:
            qubits = [machine.qAlloc() for _ in range(5)]
        setattr(collect_linear_blocks_with_and_without_limit, "_machine", machine)

    def make_linear_block(edges):
        circuit = new_block()
        for control, target in edges:
            circuit = append(circuit, cnot_gate(qubits[control], qubits[target]))
        return circuit

    def append_block_or_decompose(program, block, edges):
        try:
            return append(program, block)
        except Exception:
            for control, target in edges:
                program = append(program, cnot_gate(qubits[control], qubits[target]))
            return program

    full_edges = [(0, 1), (1, 2), (2, 3), (3, 4)]
    limited_edges_1 = [(0, 1), (1, 2)]
    limited_edges_2 = [(2, 3), (3, 4)]

    full_block = new_top()
    full_block = append(full_block, pq.H(qubits[0]))
    full_linear = make_linear_block(full_edges)
    full_block = append_block_or_decompose(full_block, full_linear, full_edges)

    limited_block = new_top()
    limited_block = append(limited_block, pq.H(qubits[0]))
    limited_linear_1 = make_linear_block(limited_edges_1)
    limited_linear_2 = make_linear_block(limited_edges_2)
    limited_block = append_block_or_decompose(limited_block, limited_linear_1, limited_edges_1)
    limited_block = append_block_or_decompose(limited_block, limited_linear_2, limited_edges_2)

    return full_block, limited_block
