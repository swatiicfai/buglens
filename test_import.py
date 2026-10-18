import sys

try:
    from google import genai
    print("google.genai imported successfully")
except Exception as e:
    print("google.genai failed:", e)

try:
    import google.generativeai as legacy_genai
    print("google.generativeai imported successfully")
except Exception as e:
    print("google.generativeai failed:", e)
