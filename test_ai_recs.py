import sys
import os

# Add the backend/app directory to the path so we can import ai_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend', 'app')))

try:
    from ai_engine import AIEngine
    import json

    engine = AIEngine()
    print("Testing AI Recommendation Engine...")
    result = engine.recommend(topic="Benefits of yoga for back pain", niche="health")

    if "error" in result:
        print(f"FAILED: {result['error']}")
    else:
        print(f"SUCCESS: Generated {len(result.get('captions', []))} captions")
        print(f"SUCCESS: Generated {len(result.get('scripts', []))} scripts")
        print("\nSCRIPTS PREVIEW:")
        for script in result.get('scripts', []):
            print(f"- {script.get('title')}: {script.get('hook')[:50]}...")
            
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
