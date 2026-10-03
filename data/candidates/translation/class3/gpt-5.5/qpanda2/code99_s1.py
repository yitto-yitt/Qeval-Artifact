# EVAL_META: task_id=99, framework=qpanda2, class=3
import math
import re
import copy
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(8)

def remove_unassigned_parameterized_gates(circuit):
    def _is_number_like(value):
        if isinstance(value, (int, float, complex, bool)):
            return True
        try:
            float(value)
            return True
        except Exception:
            return False

    def _is_unassigned_parameter(value):
        if value is None:
            return False

        if _is_number_like(value):
            return False

        if isinstance(value, str):
            try:
                eval(value, {"__builtins__": {}}, {"pi": math.pi, "PI": math.pi, "e": math.e})
                return False
            except Exception:
                return True

        try:
            params = getattr(value, "parameters", None)
            if params is not None and len(params) > 0:
                return True
        except Exception:
            pass

        try:
            free_symbols = getattr(value, "free_symbols", None)
            if free_symbols is not None and len(free_symbols) > 0:
                return True
        except Exception:
            pass

        cls_name = type(value).__name__.lower()
        mod_name = type(value).__module__.lower()
        if "parameter" in cls_name or "parameter" in mod_name:
            return True
        if cls_name in {"var", "variable", "expression"}:
            return True

        return False

    def _has_unassigned_parameters(instr):
        try:
            if hasattr(instr, "is_parameterized") and instr.is_parameterized():
                return True
        except Exception:
            pass

        params = getattr(instr, "params", None)
        if params is None:
            for name in ("get_parameters", "get_parameter", "parameters"):
                try:
                    attr = getattr(instr, name, None)
                    if callable(attr):
                        params = attr()
                        break
                except Exception:
                    pass

        if params is None:
            return False

        if isinstance(params, (list, tuple)):
            return any(_is_unassigned_parameter(param) for param in params)

        return _is_unassigned_parameter(params)

    def _unpack_instruction(instruction):
        if hasattr(instruction, "operation"):
            return instruction.operation, instruction.qubits, instruction.clbits
        return instruction[0], instruction[1], instruction[2]

    if hasattr(circuit, "data"):
        try:
            new_circuit = circuit.copy_empty_like()
        except Exception:
            try:
                new_circuit = type(circuit)(circuit.num_qubits, circuit.num_clbits)
            except Exception:
                new_circuit = type(circuit)()

        q_index = {}
        c_index = {}
        try:
            q_index = {bit: i for i, bit in enumerate(circuit.qubits)}
            c_index = {bit: i for i, bit in enumerate(circuit.clbits)}
        except Exception:
            pass

        for instruction in list(circuit.data):
            instr, qargs, cargs = _unpack_instruction(instruction)
            if _has_unassigned_parameters(instr):
                continue

            mapped_qargs = qargs
            mapped_cargs = cargs
            try:
                if q_index and hasattr(new_circuit, "qubits"):
                    mapped_qargs = [new_circuit.qubits[q_index[q]] for q in qargs]
                if c_index and hasattr(new_circuit, "clbits"):
                    mapped_cargs = [new_circuit.clbits[c_index[c]] for c in cargs]
            except Exception:
                mapped_qargs = qargs
                mapped_cargs = cargs

            new_circuit.append(instr, mapped_qargs, mapped_cargs)

        return new_circuit

    try:
        prog = circuit
        if type(circuit).__name__ == "QCircuit":
            prog = pq.QProg()
            prog << circuit

        originir = pq.convert_qprog_to_originir(prog, machine)
        filtered_lines = []
        allowed_tokens = {
            "pi", "PI", "e", "sin", "cos", "tan", "asin", "acos", "atan",
            "sqrt", "exp", "ln", "log", "pow"
        }

        for line in originir.splitlines():
            remove_line = False
            for expr in re.findall(r"\(([^()]*)\)", line):
                for token in re.findall(r"[A-Za-z_]\w*", expr):
                    if token not in allowed_tokens:
                        remove_line = True
                        break
                if remove_line:
                    break
            if not remove_line:
                filtered_lines.append(line)

        return pq.convert_originir_to_qprog("\n".join(filtered_lines), machine)
    except Exception:
        try:
            return copy.deepcopy(circuit)
        except Exception:
            return circuit

if __name__ == "__main__":
    machine.finalize()
