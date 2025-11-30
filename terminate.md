cd /home/ubuntu/yellow/backend && source venv/bin/activate && python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload


pkill -f "uvicorn app:app" && pkill -f "vite" && sleep 1 && echo "Stopped all services"


cd /home/ubuntu/yellow/frontend && npm run dev