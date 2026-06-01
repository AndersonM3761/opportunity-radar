import asyncio
import os
from app.agent.search_agent import process_profile

async def main():
    profile = {
        "branch": "Mechatronics Engineering",
        "year": "3rd Year",
        "interests": "Embedded Systems, PCB Design, PLC / HMI / SCADA",
        "goal": "Core / Hardware Engineer",
        "mode": "Any",
        "duration": "Any",
        "location": "",
        "budget": "Free only",
        "categories": ["Hackathon", "Internship", "Certification", "Competition"]
    }
    print("Running process_profile...")
    try:
        result = await process_profile(profile)
        print(f"Generated {len(result.opportunities)} opportunities")
    except Exception as e:
        print(f"FAILED WITH EXCEPTION: {e}")

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    asyncio.run(main())
