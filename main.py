import requests
import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 你的 Telegram Bot Token（請勿外流）
TOKEN = "7326636597:AAFsByDfuXucgAIrtfbYsfm5ZAsdhduawSg"

# 自訂顯示匯率（利潤價）
custom_rates = {
    "TWD": 32.00,
    "CNY": 7.20
}

# 啟動歡迎指令
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "歡迎使用 GENESIS FX 全球匯率機器人\n"
        "指令範例：\n"
        "/rate USD 查詢美元匯率\n"
        "/convert 100 USD to TWD 進行匯率換算"
    )

# 查詢單一幣別匯率
async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        code = context.args[0].upper()
        url = "https://api.exchangerate.host/latest?base=USD"
        response = requests.get(url).json()
        official = response["rates"].get(code)

        if not official:
            await update.message.reply_text("無法查詢此幣別，請確認代碼正確（如 USD、TWD、CNY）")
            return

        custom = custom_rates.get(code, round(official, 2))
        msg = f"【{code} 匯率】\n官方：1 USD = {official}\nGENESIS 報價：1 USD = {custom}"
        await update.message.reply_text(msg)

    except Exception as e:
        await update.message.reply_text("請輸入正確格式：/rate USD")

# 幣別轉換
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(context.args[0])
        from_currency = context.args[1].upper()
        to_currency = context.args[3].upper()
        url = f"https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}"
        response = requests.get(url).json()
        result = response["result"]
        await update.message.reply_text(f"{amount} {from_currency} = {round(result, 2)} {to_currency}")

    except:
        await update.message.reply_text("請使用正確格式：/convert 100 USD to TWD")

# 主程式執行
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rate", rate))
    app.add_handler(CommandHandler("convert", convert))
    app.run_polling()
