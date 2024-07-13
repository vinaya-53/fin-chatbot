import spacy
import os
from botocore.vendored import requests

def load_spacy_model():
    model_path = "/var/task/en_core_web_md"  # Adjusted for Vercel's environment
    try:
        nlp = spacy.load(model_path)
    except OSError:
        # Download the model if not available
        try:
            spacy.cli.download("en_core_web_md")
            nlp = spacy.load(model_path)
        except Exception as e:
            print(f"Error loading SpaCy model: {e}")
            nlp = None
    return nlp

def handler(event, context):
    nlp = load_spacy_model()
    if not nlp:
        return {
            "statusCode": 500,
            "body": "Error loading SpaCy model"
        }
    
    # Use nlp object for processing
    return {
        "statusCode": 200,
        "body": "SpaCy model loaded successfully"
    }
import google.cloud.dialogflow_v2  as dialogflow
from proto.marshal.collections import MapComposite
from google.protobuf import struct_pb2
import requests
import json
import math
import re
import subprocess
from pathlib import Path


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\vinuu\\fi-chatbot-rdcm-e44426a9c278.json"

ALPHA_VANTAGE_API_KEY = "5QJVB1470YSOAI6Q"
def get_stock_price(symbol):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "Time Series (1min)" in data:
            latest_time = list(data["Time Series (1min)"].keys())[0]
            latest_price = data["Time Series (1min)"][latest_time]["1. open"]
            return latest_price
        else:
            return None
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except Exception as err:
        print(f"Other error occurred: {err}")
        return None

def get_stock_info_from_api(symbol):
    try:
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        trading_volume = data.get("Volume")
        market_cap = data.get("MarketCapitalization")
        return trading_volume, market_cap
    except requests.exceptions.RequestException as err:
        print(f"Error fetching stock information: {err}")
        return None, None


def parse_duration(duration):
    # Duration in format "3 years 5 months", "2 months", etc.
    years = 0
    months = 0
    # Use regular expressions to extract numeric value and unit
    matches = re.findall(r'(\d+(\.\d+)?)\s+(\w+)', duration)
    for amount, _, unit in matches:
        amount = float(amount)
        if 'year' in unit or 'yr' in unit:
            years = int(amount)
        elif 'month' in unit or 'mo' in unit:
            months += int(amount)

    total_months = years * 12 + months
    return total_months

def extract_repayperiod(repayperiod):
    if isinstance(repayperiod, MapComposite):
        try:
            amount = repayperiod.get('amount')
            unit = repayperiod.get('unit')

            if amount is not None and unit is not None:
                amount = float(amount)
                unit = str(unit)
                return f"{amount} {unit}"
            else:
                raise ValueError("Missing 'amount' or 'unit' in repayment period.")
        except Exception as e:
            print(f"Error extracting repayperiod: {e}")
            raise ValueError("Invalid repayment period format")
    elif isinstance(repayperiod, str):
        return repayperiod
    else:
        raise ValueError("Invalid repayment period format")


def generate_loan_advice(loantype, loanamount, repayperiod):
    num_payments = parse_duration(repayperiod)
    interest_rate = 5  # Default interest rate
    monthly_rate = interest_rate / 100 / 12
    if num_payments == 0:
        return "Error: Invalid repayment period. Please provide a valid duration."

    try:
        monthly_payment = loanamount * monthly_rate / (1 - math.pow(1 + monthly_rate, -num_payments))
        total_interest = monthly_payment * num_payments - loanamount
    except ZeroDivisionError:
        return "Error: Invalid loan parameters. Please provide valid values for loan amount and repayment period."

    advice = f"For a {loantype} loan of ${loanamount} over {num_payments // 12} years {num_payments % 12} months:\n"
    advice += f"- Your estimated monthly payment would be ${monthly_payment:.2f}.\n"
    advice += f"- The total interest payable over the life of the loan would be ${total_interest:.2f}.\n"
    advice += "- Paying an extra $100 per month could save you money in interest and shorten your loan term."
    
    comparison_interest_rate = 10 if loantype.lower() == "personal loan" else 5
    comparison_payment = loanamount * (comparison_interest_rate / 100 / 12) / (1 - math.pow(1 + (comparison_interest_rate / 100 / 12), -num_payments))
    advice += f"- Compared to a {comparison_interest_rate}% interest rate, your monthly payment is {'lower' if monthly_payment < comparison_payment else 'higher'}."
    
    return advice

def generate_stock_advice(stock_symbol, price, market_cap):
    price = float(price)
    market_cap = float(market_cap)
    advice = ""
    if market_cap > 1000000000:
        advice += "This company has a large market cap, indicating it is a well-established company."
    elif market_cap > 500000000:
        advice += "This company has a medium market cap, indicating it is a growing company."
    else:
        advice += "This company has a small market cap, indicating it may be a newer or less established company."

    if price < 50:
        advice += "\nThe stock price is relatively low, which might be an opportunity for investment."
    elif price < 150:
        advice += "\nThe stock price is moderate, suggesting it has room for growth."
    else:
        advice += "\nThe stock price is high, which might indicate it is well-valued by the market."

    return advice

def detect_intent_texts(texts):
    session_id = "unique-session-id"
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path("fi-chatbot-rdcm", session_id)

    all_responses = []

    for text in texts:
        text_input = dialogflow.types.TextInput(text=text, language_code="en")
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)

        if response.query_result.intent.display_name == "getstockprice":
            parameters = response.query_result.parameters
            company_name = parameters.get("company")
            if company_name:
                stock_symbol = company_name
                price = get_stock_price(stock_symbol)
                if price:
                    trading_volume, market_cap = get_stock_info_from_api(stock_symbol)
                    if market_cap is not None:
                        response_text = f"The current price of {stock_symbol} is ${price}. \n and the market capitalization is ${market_cap}."
                        response_text +=  generate_stock_advice(stock_symbol, price, market_cap)
                    else:
                        response_text = f"The current price of {stock_symbol} is ${price}."
                else:
                    response_text = f"Sorry, I couldn't fetch the price for {stock_symbol} at the moment. Please try again later."
            else:
                response_text = "Please specify a stock symbol to get its current price."

        elif response.query_result.intent.display_name == "loanadvisor":
            parameters = response.query_result.parameters
            loantype = parameters.get("loantype")
            loanamount = parameters.get("loanamount")
            repayperiod = parameters.get("repayperiod")
            loantype = loantype if loantype else None
            loanamount = float(loanamount) if loanamount else None
            repayperiod = extract_repayperiod(repayperiod) if repayperiod else None

            if loantype and loanamount and repayperiod:
                response_text = generate_loan_advice(loantype, loanamount, repayperiod)
            else:
                missing_params = []
                if not loantype:
                    missing_params.append("loan type")
                if not loanamount:
                    missing_params.append("loan amount")
                if not repayperiod:
                    missing_params.append("repayment period")

                response_text = f"Please provide the following missing information: {', '.join(missing_params)}."

        else:
            response_text = response.query_result.fulfillment_text

        all_responses.append(response_text)

    return all_responses

# Example usage
def chatbot_response(user_input):
    doc = nlp(user_input)
    responses = detect_intent_texts([user_input])  # Ensure input is a list
    if responses:
        return responses[0]  # Return the first response for simplicity
    return "Sorry, I couldn't understand that."
