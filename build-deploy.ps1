echo "Building frontend..."
cd frontend
npm run build

echo ""
echo "Deploying to GitHub Pages..."
cd dist
git init
git add .
git commit -m "Deploy AI Customer Service"
git push --force https://github.com/2587958021/AI-CustomerService.git master:gh-pages

echo ""
echo "Done! Visit: https://2587958021.github.io/AI-CustomerService"