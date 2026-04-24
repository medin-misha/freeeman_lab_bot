from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from config import settings
from core.utils import check_sub_channel_dec, ensure_user_registered
from .buttons import (
    back_reply_keyboard,
    consultations_reply_keyboard,
    more_reply_keyboard,
    services_reply_keyboard,
    socials_inline_keyboard,
)
from .publisher import publish_consultation_request, publish_mentorship_request, publish_regression_request
from .states import MoreStates

router = Router(name="more")


@router.message(F.text.lower() == "еще возможности")
@ensure_user_registered
@check_sub_channel_dec
async def more_handler(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        text=settings.message.text.get("more_intro"),
        reply_markup=more_reply_keyboard(),
    )


@router.message(F.text.lower() == "посмотреть услуги")
@ensure_user_registered
@check_sub_channel_dec
async def services_handler(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MoreStates.services)
    await msg.answer(
        text=settings.message.text.get("services_intro"),
        reply_markup=services_reply_keyboard(),
    )


@router.message(StateFilter(MoreStates.services), F.text.lower() == "назад")
async def services_back_handler(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        text=settings.message.text.get("more_intro"),
        reply_markup=more_reply_keyboard(),
    )


@router.message(F.text.lower() == "консультации")
@ensure_user_registered
@check_sub_channel_dec
async def consultations_handler(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MoreStates.consultations)
    await msg.answer(
        text=settings.message.text.get("consultations_intro"),
        reply_markup=consultations_reply_keyboard(),
    )


@router.message(StateFilter(MoreStates.consultations), F.text.lower() == "оставить запрос")
async def consultation_request_handler(msg: types.Message, state: FSMContext) -> None:
    user = msg.from_user
    username = f"@{user.username}" if user and user.username else str(user.id if user else "")
    await publish_consultation_request({"username": username})
    await state.set_state(MoreStates.services)
    await msg.answer(
        text=settings.message.text.get("consultation_request_sent"),
        reply_markup=services_reply_keyboard(),
    )


@router.message(StateFilter(MoreStates.consultations), F.text.lower() == "назад")
async def consultations_back_handler(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MoreStates.services)
    await msg.answer(
        text=settings.message.text.get("services_intro"),
        reply_markup=services_reply_keyboard(),
    )


@router.message(F.text.lower() == "регрессии")
@ensure_user_registered
@check_sub_channel_dec
async def regressions_handler(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MoreStates.regressions)
    await msg.answer(
        text=settings.message.text.get("regressions_intro"),
        reply_markup=consultations_reply_keyboard(),
    )


@router.message(StateFilter(MoreStates.regressions), F.text.lower() == "оставить запрос")
async def regression_request_handler(msg: types.Message, state: FSMContext) -> None:
    user = msg.from_user
    username = f"@{user.username}" if user and user.username else str(user.id if user else "")
    await publish_regression_request({"username": username})
    await state.set_state(MoreStates.services)
    await msg.answer(
        text=settings.message.text.get("regression_request_sent"),
        reply_markup=services_reply_keyboard(),
    )


@router.message(StateFilter(MoreStates.regressions), F.text.lower() == "назад")
async def regressions_back_handler(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MoreStates.services)
    await msg.answer(
        text=settings.message.text.get("services_intro"),
        reply_markup=services_reply_keyboard(),
    )


@router.message(F.text.lower() == "наставничество")
@ensure_user_registered
@check_sub_channel_dec
async def mentorship_handler(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MoreStates.mentorship)
    await msg.answer(
        text=settings.message.text.get("mentorship_intro"),
        reply_markup=consultations_reply_keyboard(),
    )


@router.message(StateFilter(MoreStates.mentorship), F.text.lower() == "оставить запрос")
async def mentorship_request_handler(msg: types.Message, state: FSMContext) -> None:
    user = msg.from_user
    username = f"@{user.username}" if user and user.username else str(user.id if user else "")
    await publish_mentorship_request({"username": username})
    await state.set_state(MoreStates.services)
    await msg.answer(
        text=settings.message.text.get("mentorship_request_sent"),
        reply_markup=services_reply_keyboard(),
    )


@router.message(StateFilter(MoreStates.mentorship), F.text.lower() == "назад")
async def mentorship_back_handler(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MoreStates.services)
    await msg.answer(
        text=settings.message.text.get("services_intro"),
        reply_markup=services_reply_keyboard(),
    )


@router.message(F.text.lower() == "соцсети")
@ensure_user_registered
@check_sub_channel_dec
async def socials_handler(msg: types.Message) -> None:
    await msg.answer(
        text=settings.message.text.get("socials_intro"),
        reply_markup=socials_inline_keyboard(),
    )


@router.message(F.text.lower() == "о проекте")
@ensure_user_registered
@check_sub_channel_dec
async def about_project_handler(msg: types.Message) -> None:
    await msg.answer(
        text=settings.message.text.get("about_project_intro"),
        reply_markup=back_reply_keyboard(),
    )


@router.message(F.text.lower() == "магазин")
@ensure_user_registered
@check_sub_channel_dec
async def shop_handler(msg: types.Message, state: FSMContext) -> None:
    await state.set_state(MoreStates.shop)
    await msg.answer(
        text=settings.message.text.get("shop_intro"),
        reply_markup=back_reply_keyboard(),
    )


@router.message(StateFilter(MoreStates.shop), F.text.lower() == "назад")
async def shop_back_handler(msg: types.Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        text=settings.message.text.get("more_intro"),
        reply_markup=more_reply_keyboard(),
    )
