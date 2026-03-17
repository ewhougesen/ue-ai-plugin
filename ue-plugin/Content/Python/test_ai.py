"""
Simple test for UE AI Plugin
Run this in Unreal Python console
"""

import unreal

def test_backend():
    """Test if backend is running"""
    import http.client
    try:
        conn = http.client.HTTPConnection("localhost", 8000)
        conn.request("GET", "/health")
        response = conn.getresponse()

        if response.status == 200:
            unreal.log("✅ Backend is running!")
            return True
        else:
            unreal.log_error(f"❌ Backend error: {response.status}")
            return False
    except Exception as e:
        unreal.log_error(f"❌ Cannot connect to backend: {e}")
        return False

def create_test_cube():
    """Create a test cube"""
    import ue_ai_plugin
    result = ue_ai_plugin.create_cube("TestCube", (100, 100, 100))
    unreal.log(f"✅ Created cube: {result}")
    return result

# Run tests
unreal.log("=" * 50)
unreal.log("UE AI Plugin - Test Script")
unreal.log("=" * 50)

test_backend()

unreal.log("")
unreal.log("Type 'create_test_cube()' to make a cube")
unreal.log("=" * 50)
