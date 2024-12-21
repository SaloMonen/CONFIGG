import sys
import yaml


class VirtualMachine:
    def __init__(self):
        self.memory = [0] * 256  # Объем памяти
        self.registers = [0] * 16  # 16 регистров

    def load_binary(self, binary_file):
        with open(binary_file, 'rb') as f:
            self.program = f.read()

    def execute(self, output_file, memory_range):
        results = []
        idx = 0
        while idx < len(self.program):
            A = self.program[idx]
            B = (self.program[idx + 1] << 8) | self.program[idx + 2]
            C = (self.program[idx + 3] << 8) | self.program[idx + 4]

            if A == 30:  # LOAD_CONST
                self.registers[C] = B
            elif A == 8:  # READ_MEM
                self.registers[B] = self.memory[C]
            elif A == 11:  # WRITE_MEM
                self.memory[B] = self.registers[C]
            elif A == 39:  # POPCNT
                self.registers[B] = bin(self.registers[C]).count('1')

            # Сохраняем результат в указанный диапазон памяти
            if idx < memory_range:
                results.append(self.registers[B])

            idx += 5

        # Сохранение результата в файл YAML
        with open(output_file, 'w') as f:
            yaml.dump(results, f)


if __name__ == "__main__":
    binary_file = sys.argv[1]
    output_file = sys.argv[2]
    memory_range = int(sys.argv[3])

    vm = VirtualMachine()
    vm.load_binary(binary_file)
    vm.execute(output_file, memory_range)