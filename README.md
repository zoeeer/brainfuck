# A Brainfuck Interpreter (implemented with python)

## Brainfuck Background
https://en.wikipedia.org/wiki/Brainfuck

### Commands
The eight language commands each consist of a single character:


| Character | Meaning |
| --------- | --------- |
| > | Increment the data pointer (to point to the next cell to the right). |
| < | Decrement the data pointer (to point to the next cell to the left). |
| + | Increment (increase by one) the byte at the data pointer. |
| - | Decrement (decrease by one) the byte at the data pointer. |
| . | Output the byte at the data pointer. |
| , | Accept one byte of input, storing its value in the byte at the data pointer. |
| [ | If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command. |
| ] | If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command. |

## Tests
### Basic
- helloworld.txt (source: [Hello World in Brainfuck](https://therenegadecoder.com/code/hello-world-in-brainfuck/))
- echo.txt
### Torture Test
Tested with some interesting programs from the [Brainfuck torture test](https://github.com/rdebath/Brainfuck).
- Hello.b
- Hello2.b
- bitwidth.b
- fibint.b (needs 8-bits machine)
- Mandelbrot-tiny.b

## How To Run
1. Run commands directly
    ```sh
    python vm.py -c ",[.,]"  # give instructions on command line
    ```

2. Run file
    ```sh
    python vm.py helloworld.txt  # run a file
    ```

3. Run with limited bitwidth
    ```sh
    python vm.py -b 8 bitwidth.b  # run as 8-bits machine (bitwidth.b comes from the torture test set)
    ```

