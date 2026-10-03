# EVAL_META: task_id=110, framework=pennylane, class=3
import pennylane as qml

def equivalent_clifford_circuit(circuit, n):
    if isinstance(circuit, qml.QNode):
        is_qnode = True
        is_tape = False
    elif isinstance(circuit, qml.tape.QuantumTape):
        is_qnode = False
        is_tape = True
    else:
        is_qnode = False
        is_tape = False

    if is_qnode:
        wires = list(circuit.device.wires)
    elif is_tape:
        wires = list(circuit.wires)
    else:
        wires = [0]
    
    wire = wires[0] if wires else 0

    qc_list = []
    for i in range(n):
        if is_qnode:
            def make_func(idx):
                def new_func(*args, **kwargs):
                    circuit.func(*args, **kwargs)
                    if idx % 4 == 0:
                        qml.Hadamard(wires=wire)
                        qml.Hadamard(wires=wire)
                    elif idx % 4 == 1:
                        qml.PauliX(wires=wire)
                        qml.PauliX(wires=wire)
                    elif idx % 4 == 2:
                        qml.S(wires=wire)
                        qml.S(wires=wire)
                        qml.S(wires=wire)
                        qml.S(wires=wire)
                    else:
                        qml.PauliY(wires=wire)
                        qml.PauliY(wires=wire)
                return new_func
            qc_list.append(qml.QNode(make_func(i), circuit.device))
        elif is_tape:
            ops = list(circuit.operations)
            if i % 4 == 0:
                extra = [qml.Hadamard(wires=wire), qml.Hadamard(wires=wire)]
            elif i % 4 == 1:
                extra = [qml.PauliX(wires=wire), qml.PauliX(wires=wire)]
            elif i % 4 == 2:
                extra = [qml.S(wires=wire), qml.S(wires=wire), qml.S(wires=wire), qml.S(wires=wire)]
            else:
                extra = [qml.PauliY(wires=wire), qml.PauliY(wires=wire)]
            
            new_tape = qml.tape.QuantumTape(ops + extra, circuit.measurements)
            qc_list.append(new_tape)
        else:
            def make_func(idx):
                def new_func(*args, **kwargs):
                    circuit(*args, **kwargs)
                    if idx % 4 == 0:
                        qml.Hadamard(wires=wire)
                        qml.Hadamard(wires=wire)
                    elif idx % 4 == 1:
                        qml.PauliX(wires=wire)
                        qml.PauliX(wires=wire)
                    elif idx % 4 == 2:
                        qml.S(wires=wire)
                        qml.S(wires=wire)
                        qml.S(wires=wire)
                        qml.S(wires=wire)
                    else:
                        qml.PauliY(wires=wire)
                        qml.PauliY(wires=wire)
                return new_func
            qc_list.append(make_func(i))
            
    return qc_list
