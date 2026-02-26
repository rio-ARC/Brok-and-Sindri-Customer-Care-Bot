# Brok & Sindri Customer Care Bot

I was inspired to build this while watching the gameplay of *God of War* and wanting to learn LangChain and LangGraph better. The dual-persona mechanic of Brok (rude, technical genius) and Sindri (anxious, polite) seemed perfect for a quirky customer support bot. **Next up:** Connecting the newly built React frontend to the FastAPI backend!

**🔥 [TRY THE LIVE BOT HERE](https://brok-and-sindri-customer-care-bot.onrender.com/docs) (Swagger UI)**

## What's Done

### Backend
- **LangGraph StateGraph** with intent classification (Technical / Billing / Feedback)
- **ReAct agents** for Billing and Technical nodes with tool execution
- **Tools:** Order lookup, server diagnostics (psutil), web search (Tavily)
- **FastAPI backend** with `/chat` endpoint
- **User memory** with thread-based sessions (each user_id maintains separate conversation history)
- **Dual-persona responses** — every reply features both Brok and Sindri interacting

### Frontend
- **Next.js & Tailwind CSS UI** matching a God of War forge environment
- **Glassmorphism chat interface** utilizing strict z-index layering to preserve character visibility
- **Responsive design** that scales character assets and adapts gracefully to mobile screens
- **Custom themed message bubbles** distinguishing between the user and the Brok/Sindri bot
