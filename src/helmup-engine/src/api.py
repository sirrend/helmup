from fastapi import FastAPI
from main import main_handler
from shared_packages.gpt_cost_calculator import print_total_program_gpt_costs
from utils import Item
from json import dumps


app = FastAPI()

@app.post("/upgrade")
def create_item(item: Item):
    results = main_handler(item)
    print_total_program_gpt_costs()

    return results

@app.get("/healthcheck")
def healthcheck():
    return dumps({"status": "alive"}), 200

# Run the FastAPI server with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
