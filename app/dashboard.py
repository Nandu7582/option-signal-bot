def show_dashboard(signals):
    for signal in signals:
        st.markdown(f"### {signal['asset']} – {signal['symbol']}")
        st.success(f"BUY @ ₹{signal['price']}")
        st.write(f"🎯 Target: ₹{signal['target']} | 🛑 SL: ₹{signal['stop_loss']}")
        if signal['hedge']:
            st.write(f"💰 Hedge: {signal['hedge']}")
        st.write(f"🧠 Logic: {signal['logic']}")
        st.image("app/static/pl_graph.png")
