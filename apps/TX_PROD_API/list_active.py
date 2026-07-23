from pathlib import Path
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

SOAP_URL = "http://172.31.87.2:20011"

INPUT_FILE = Path("input").glob("*.xlsx")
INPUT_FILE = next(INPUT_FILE)

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

HEADERS = {
    "Content-Type": "text/xml; charset=utf-8"
}

session = requests.Session()

SOAP_TEMPLATE = """<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <tw:Tran xmlns:tw="http://schemas.tranzaxis.com/tran.wsdl"
             xmlns:tran="http://schemas.tranzaxis.com/tran.xsd">
      <tran:Request xmlns:card="http://schemas.tranzaxis.com/tokens-admin.xsd"
                    xmlns:tran="http://schemas.tranzaxis.com/tran.xsd"
                    xmlns:com="http://schemas.tranzaxis.com/common-types.xsd"
                    xmlns:ctrt="http://schemas.tranzaxis.com/contracts-admin.xsd"
                    InitiatorRid="MBTURON"
                    LifePhase="Single"
                    Kind="ModifyToken">

        <tran:Specific>
          <tran:Admin>
            <tran:Token>
              <card:Card>
                <card:Status>Active</card:Status>
                <card:ExtRid>{card}</card:ExtRid>
              </card:Card>
            </tran:Token>
          </tran:Admin>
        </tran:Specific>

      </tran:Request>
    </tw:Tran>
  </soap:Body>
</soap:Envelope>
"""


def activate(card):

    xml = SOAP_TEMPLATE.format(card=card)

    try:

        response = session.post(
            SOAP_URL,
            data=xml.encode("utf-8"),
            headers=HEADERS,
            timeout=20,
        )

        if response.status_code == 200:

            text = response.text

            if "Fault" in text:
                return card, "ERROR", text[:500]

            return card, "SUCCESS", ""

        return card, "HTTP_ERROR", response.text[:500]

    except Exception as e:
        return card, "EXCEPTION", str(e)


df = pd.read_excel(INPUT_FILE)

cards = (
    df["#"]
    .astype(str)
    .str.strip()
    .tolist()
)

results = []

with ThreadPoolExecutor(max_workers=20) as executor:

    futures = [executor.submit(activate, c) for c in cards]

    for future in as_completed(futures):
        results.append(future.result())

result_df = pd.DataFrame(
    results,
    columns=[
        "Card",
        "Status",
        "Message"
    ]
)

success = result_df[result_df.Status == "SUCCESS"]
errors = result_df[result_df.Status != "SUCCESS"]

success.to_excel(
    OUTPUT_DIR / "success.xlsx",
    index=False,
)

errors.to_excel(
    OUTPUT_DIR / "errors.xlsx",
    index=False,
)

print("=" * 40)
print("TOTAL :", len(result_df))
print("SUCCESS :", len(success))
print("ERROR :", len(errors))
print("=" * 40)