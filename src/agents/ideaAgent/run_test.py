import asyncio
from ideaAgent import IdeaAgent

async def main():
    await IdeaAgent.test()

if __name__ == "__main__":
    asyncio.run(main()) 