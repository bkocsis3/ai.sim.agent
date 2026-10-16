import asyncio
from cli.controller import Controller

async def async_input(prompt: str) -> str:
    return await asyncio.to_thread(input, prompt)

async def main():
    controller = Controller()

    print("\nController")
    print("Commands: start sim | inject ai | quit\n")

    while True:
        cmd = (await async_input(">> controller: ")).strip().lower()

        if cmd == "start sim":
            await controller.start_sim()

        elif cmd == "inject ai":
            await controller.inject_ai()

        elif cmd == "quit":
            await controller.quit()
            break

        else:
            print("\tUnknown command.")
            print("\tCommands: start sim | inject ai | quit")

if __name__ == "__main__":
    asyncio.run(main())