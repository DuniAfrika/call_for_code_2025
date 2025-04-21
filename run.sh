# Install requiremnts
pip install -r requirements.txt
echo "Requirements Installing...."

# Run app
uvicorn main:app --reload
