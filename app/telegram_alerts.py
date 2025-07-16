def send_telegram_message(signal):
    msg = f"""
📌 SIGNAL – {signal['asset']} {signal['symbol']}
🟢 BUY @ ₹{signal['price']}
🎯 Target: ₹{signal['target']} | 🛑 SL: ₹{signal['stop_loss']}
🧠 Logic: {signal['logic']}
"""
    if signal['hedge']:
        msg += f"\n💰 Hedge: {signal['hedge']}"
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                  data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
