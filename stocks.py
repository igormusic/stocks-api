import io
import csv
import json
from datetime import datetime
from bson import Decimal128
from fastapi import FastAPI, UploadFile, File
from re import sub
from fastapi.openapi.models import Response
from db import db, CustomJsonEncoder

app = FastAPI()


@app.post("/api/stock-data/bulk-insert")
async def upload(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        decoded = contents.decode()
        buffer = io.StringIO(decoded)
        stock_reader = csv.DictReader(buffer, delimiter=',')

        db.stocks.delete_many({})

        rows = []
        format_str = '%m/%d/%Y'

        for stock in stock_reader:
            row = {
                "quarter": int(stock['quarter']),
                "stock": stock['stock'],
                "date": datetime.strptime(stock['date'], format_str),
                "open": parse_money(stock, "open"),
                "high": parse_money(stock, "high"),
                "low": parse_money(stock, "low"),
                "close": parse_money(stock, "close"),
                "volume": int(stock['volume']),
                "percent_change_price": Decimal128(stock['percent_change_price']),
                "percent_change_volume_over_last_wk":
                    Decimal128("0") if stock['percent_change_volume_over_last_wk'] == ""
                    else Decimal128(stock['percent_change_volume_over_last_wk']),
                "previous_weeks_volume":
                    int("0") if stock['previous_weeks_volume'] == ""
                    else int(stock['previous_weeks_volume']),
                "next_weeks_open": parse_money(stock, "next_weeks_open"),
                "next_weeks_close": parse_money(stock, "next_weeks_close"),
                "percent_change_next_weeks_price": Decimal128(stock['percent_change_next_weeks_price']),
                "days_to_next_dividend": int(stock['days_to_next_dividend']),
                "percent_return_next_dividend": Decimal128(stock['percent_return_next_dividend'])
            }

            rows.append(row.copy())

        var = db.stocks.insert_many(rows)

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return {"message": f"{err=}"}
    finally:
        await file.close()

    return {"message": "Successfully uploaded"}


def parse_money(each, field: str):
    return Decimal128(sub(r'[^\d.]', '', each[field]))


@app.get("/api/stock-data/{stock}")
async def get(stock: str):
    result = json.dumps(
        list(
            db.stocks.find(
                {"stock": stock},
                {"_id": 0,
                 "stock": 1,
                 "date": 1,
                 "open": 1,
                 "high": 1,
                 "low": 1,
                 "close": 1,
                 "volume": 1,
                 "percent_change_price": 1,
                 "percent_change_volume_over_last_wk": 1,
                 "previous_weeks_volume": 1,
                 "next_weeks_open": 1,
                 "next_weeks_close": 1,
                 "percent_change_next_weeks_price": 1,
                 "days_to_next_dividend": 1,
                 "percent_return_next_dividend": 1})),
        cls=CustomJsonEncoder).encode('utf-8')

    json_result = json.loads(result)

    return json_result
