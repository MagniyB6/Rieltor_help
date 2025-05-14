from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from services.gpt import generate_post_text
from utils.limiter import check_and_decrease_limit

router = Router()

# --- FSM States ---
class ContentStates(StatesGroup):
    waiting_for_idea = State()


# --- Команда /контент ---
@router.message(F.text == "/контент")
async def start_content_generation(message: Message, state: FSMContext):
    await message.answer(
        "✨ Отлично! Давай я помогу тебе сделать контент для соцсетей 👀\n\n"
        "Можем рассказать про:\n"
        "- интересную сделку,\n"
        "- крутой объект,\n"
        "- свежую новость,\n"
        "— или просто твои мысли, как риелтора.\n\n"
        "💡 Напиши, про что ты бы сегодня хотел рассказать — я это докручу и выдам тебе готовый текст ✨"
    )
    await state.set_state(ContentStates.waiting_for_idea)


# --- FSM Ответ на идею ---
@router.message(ContentStates.waiting_for_idea)
async def handle_idea(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not check_and_decrease_limit(user_id, action="post"):
        await message.answer("⛔ У тебя закончились доступные генерации постов. Попробуй завтра или пополни лимит.")
        return

    await message.answer("💭 Думаю над текстом...")
    result = await generate_post_text(message.text)
    await message.answer(f"🎉 Вот твой текст:\n\n{result}")
    await state.clear()
