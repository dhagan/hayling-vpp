from playwright.sync_api import sync_playwright

TARGET_URL = (
    "https://live.tractrac.com/viewer/index.html?target="
    "https://em.liveserver1.tractrac.com/events/"
    "2f630e20-fa12-013e-aa84-04421a259aad/races/"
    "a656b180-5787-013f-c3b9-04421a259aad.json"
)


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="chrome", headless=False)
        page = browser.new_page()
        responses = []
        websockets = []

        def record_response(response):
            if ".mtb" in response.url or response.url.endswith(
                "a656b180-5787-013f-c3b9-04421a259aad.json"
            ):
                responses.append(response)

        page.on("response", record_response)
        page.on("websocket", lambda websocket: websockets.append(websocket.url))
        page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60000)
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        page.wait_for_timeout(3000)

        print("Title:", page.title())
        print("9252 row:")
        for line in page.locator("body").inner_text().splitlines():
            if "9252" in line:
                print(line.strip())

        print("WebSockets:")
        for websocket_url in websockets:
            print(" ", websocket_url)
        if not websockets:
            print("  none observed")

        print("Race-data responses:")
        for response in responses:
            try:
                body = response.body()
                size = len(body)
                prefix = body[:32].hex(" ")
            except Exception as error:
                size = "unavailable"
                prefix = str(error)
            print(f"  HTTP {response.status} {response.url}")
            print(f"    type={response.headers.get('content-type')} bytes={size}")
            print(f"    first bytes={prefix}")

        input("Press Enter to close the browser...")
        browser.close()


if __name__ == "__main__":
    main()
