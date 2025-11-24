import subprocess
import sys

def main():
    print("To run the Streamlit application, execute the following command in your terminal:")
    print("streamlit run ui/streamlit_app.py")
    print("\nMake sure you have all dependencies installed by running 'uv sync'")
    
    # Optional: Automatically run the streamlit app
    # You might want to uncomment the following lines if you want the app to start automatically
    # try:
    #     subprocess.run(["streamlit", "run", "ui/streamlit_app.py"])
    # except FileNotFoundError:
    #     print("Streamlit is not found. Please ensure it's installed and in your PATH.")
    # except Exception as e:
    #     print(f"An error occurred while trying to run Streamlit: {e}")


if __name__ == "__main__":
    main()
