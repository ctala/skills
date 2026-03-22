import time
import json
import os
from longbridge.openapi import Config, TradeContext, OrderType, OrderSide, TimeInForceType
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# 配置路径
HISTORY_FILE = "/home/admin/.openclaw/skills/my_longbridge_mgnt_skill/order_history.json"

# API 凭证 (应使用安全 vault)
APP_KEY = "1ab56e0d711bf492491a795fd088170f"
APP_SECRET = "6f9285faff4b8aec2e6de8fc4fdb67f0f08426c7ba9a92fc9b041f9151b9f111"
ACCESS_TOKEN = "m_eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ5YWRiMGIxYTdlNzYxNzEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJsb25nYnJpZGdlIiwic3ViIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNzgxMDE5Njc3LCJpYXQiOjE3NzMyNDM2NzksImFrIjoiMWFiNTZlMGQ3MTFiZjQ5MjQ5MWE3OTVmZDA4ODE3MGYiLCJhYWlkIjoyMDUzMjY1MCwiYWMiOiJsYl9wYXBlcnRyYWRpbmciLCJtaWQiOjE2MTg0MzksInNpZCI6ImJmSDV6SUNpL0Rwc3ViK050T1I3akE9PSIsImJsIjozLCJ1bCI6MCwiaWsiOiJsYl9wYXBlcnRyYWRpbmdfMjA1MzI2NTAifQ.OG-mJZpPtEMy-j_6bBnh8rrw_i_VVOuu1XsuAY4yDGcpjXTEFDKe_l-OH853hc5JDmfQFRDb1SBc5bB_Gj4zsPFKtpHqP0Ogyuj7vwvtk6iwVmm4ubAImYhx8HaRwMsowglEaUm0jwQrI1yLmyw2yI3nPJQ43Ai_fvFIJifN907LOk7nrhNxyTOo6EKRE29qfBu4w6EeE9b0vK7Gq25nTwQ2N5xprZSplZkNTUg2t1QdlFXVgrjvWP44JFkYegEJgg8EGFKfx_CaYGFgRO8z1GwM9GilhIHj9d7YLBn3WRhdO22_rsH46YcXOhpIXxwlUNQSdf3fqyhglG_rd6Vveg3GvPEKfSPpxjUadAqKth61d13bjRMX3LAgaeR4oM7tV1tep6MH5r5w1pNMOjX51Ac8p6Z0-fLFDJ45qRmk3RFoR6NjgTXB-E5NBfC36WNJKgSzerUeQE3KbO8ob-McY1jymQ4yfCuv4BSEM0NJrTEdYsKDDhsvfQ15DGQP2VCm5Myg6YRt9rG0OvSLsTdXD73OtGyU-0lBJdrPs9eTIcp_Ldp2cREea-SOQiNcsOQ-nNhI2PCulsgtgsfws77strdwgNb6QyEXVQRsU4LGcKHEdNeAmKzi6yAnNBrBAGOevgudk8yHae3l79LmZoxwPDTc6PyFOuFazMadMDjGA-c"

def get_trade_context():
    config = Config.from_apikey(app_key=APP_KEY, app_secret=APP_SECRET, access_token=ACCESS_TOKEN)
    return TradeContext(config)

def is_duplicate_order(symbol, side, quantity):
    if not os.path.exists(HISTORY_FILE):
        return False
    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)
    
    now = time.time()
    # 检查 60 秒内是否有相同订单
    for entry in history:
        if (entry["symbol"] == symbol and entry["side"] == str(side) and 
            entry["quantity"] == quantity and (now - entry["time"] < 60)):
            return True
    return False

def save_order(symbol, side, quantity):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    
    history.append({"symbol": symbol, "side": str(side), "quantity": quantity, "time": time.time()})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def execute_order_with_retry(trade, symbol, side, quantity):
    return trade.submit_order(symbol=symbol, order_type=OrderType.MO, side=side, submitted_quantity=quantity, time_in_force=TimeInForceType.Day)

def has_pending_order(trade, symbol, side, quantity):
    orders = trade.today_orders()
    # 查找最近的相同订单
    for order in orders:
        if order.symbol == symbol and str(order.side) == str(side) and order.submitted_quantity == quantity:
            if order.status in ["Submitted", "Pending"]:
                return True
    return False

def manage_order(action, symbol=None, quantity=None, order_id=None, side=None, force=False):
    if action == "sell" or action == "buy":
        if not force and is_duplicate_order(symbol, str(side), quantity):
            print("DUPLICATE_CONFIRMATION_REQUIRED")
            return
        
        trade = get_trade_context()
        # 增加服务器端重复检查
        if has_pending_order(trade, symbol, side, quantity):
            print("SERVER_SIDE_DUPLICATE_DETECTED: 存在同向待成交订单")
            return

        resp = trade.submit_order(symbol=symbol, order_type=OrderType.MO, side=side, submitted_quantity=quantity, time_in_force=TimeInForceType.Day)
        oid = resp.order_id
        save_order(symbol, str(side), quantity)
        time.sleep(2)
        detail = trade.order_detail(order_id=oid)
        print(f"订单提交成功, ID: {oid}, 状态: {detail.status}")
