echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt

echo ""
echo "Installing frontend dependencies..."
cd ..\frontend
npm install

echo ""
echo "Installation complete!"
echo "Please edit backend/.env and add your ZHIPU_API_KEY"
