import asyncio
from game_controller.controller import GameController

async def async_input(prompt: str) -> str:
    return await asyncio.to_thread(input, prompt)

async def main():
    controller = GameController()

    print("\nGame Controller CLI")
    print("Commands: start game | inject ai | quit\n")

    while True:
        cmd = (await async_input(">> game controller: ")).strip().lower()

        if cmd == "start game":
            await controller.start_game()

        elif cmd == "inject ai":
            await controller.inject_ai()

        elif cmd == "quit":
            await controller.quit()
            break

        else:
            print("\tUnknown command.")
            print("\tCommands: start game | inject ai | quit")

if __name__ == "__main__":
    asyncio.run(main())