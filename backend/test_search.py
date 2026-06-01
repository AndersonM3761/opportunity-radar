import asyncio
import os
from app.agent.search_agent import process_profile

async def main():
    profile = {
        "branch": "Computer Science Engineering",
        "year": "2nd Year",
        "interests": "Machine Learning, Computer Vision",
        "goal": "Software Engineer",
        "mode": "Any",
        "duration": "Any",
        "location": "",
        "budget": "Free only",
        "categories": ["Hackathon", "Internship", "Certification", "Competition"]
    }
    print("Running process_profile...")
    result = await process_profile(profile)
    print(f"Generated {len(result.opportunities)} opportunities")
    for opp in result.opportunities:
        print(f"- {opp.name} ({opp.deadline})")

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    asyncio.run(main())
