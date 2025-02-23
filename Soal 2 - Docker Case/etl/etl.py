import asyncio
import httpx

sentences = [
    "Saya suka makan nasi goreng.",
    "Hari ini cuaca sangat panas.",
    "Anjing itu sangat lucu.",
    "Kami akan pergi ke pantai besok.",
    "Apakah kamu punya hobi?",
    "Buku ini sangat menarik untuk dibaca.",
    "Sekarang waktunya istirahat.",
    "Kucing itu tidur di bawah meja.",
    "Makanan favorit saya adalah rendang.",
    "Kami berencana untuk berlibur ke Bali.",
]

api_url = "http://api:6000/predict"

async def process_sentences():
    for sentence in sentences:
        try:
            async with httpx.AsyncClient() as aclient:
                response = await aclient.post(api_url, params={"text": sentence})

                if response.status_code == 422:
                    print(f"422 Error: {response.json()}")
                else:
                    response.raise_for_status()

                print(f"Response for sentence '{sentence}': {response.json()}")

        except httpx.RequestError as exc:
            print(f"Request failed: {exc}")
            continue
        except httpx.HTTPStatusError as exc:
            print(f"HTTP error occurred: {exc}")
            continue
        except Exception as e:
            print(f"Unexpected error: {e}")
            continue

async def main():
    while True:  # Ensure the script keeps running
        await process_sentences()
        print("Retrying in 5 seconds...")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
