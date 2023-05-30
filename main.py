from geopy.geocoders import Nominatim

from config import BOT_TOKEN
import logging
from buttons import register_markup, the_registerator_button, cancel_markup
from states import RegisterStates
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
bot = Bot(token=BOT_TOKEN, parse_mode="html")
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start"], state='*')
async def do_start(message: types.Message, state:FSMContext):
    await state.finish()
    user = message.from_user.full_name
    await message.reply(f"Assalomu alaykum {user} xush kelibsiz! kerakli bo'limni tanlang", reply_markup=register_markup)

@dp.message_handler(commands=["help"])
async def do_help(message: types.Message):
    user = message.from_user.full_name
    await message.reply(text=f"Sizga qanday yordam bera olaman {user}")


@dp.message_handler(text = "❎ Bekor Qilish", state="*")
async def start_register(message: types.Message, state:FSMContext):
    await state.finish()
    await message.reply(f"Assalomu alaykum {message.from_user.full_name} xush kelibsiz! kerakli bo'limni tanlang", reply_markup=register_markup)

@dp.message_handler(text = "✅ Qabul Qilish", state="*")
async def start_register(message: types.Message, state:FSMContext):
    await state.finish()
    await message.reply(f"<b>{message.from_user.full_name}</b> sizning ma'lumotlaringiz saqlab qolindi", reply_markup=register_markup)
    data = await state.get_data()
    full_name = data.get("full_name")
    passport = data.get("passport")
    age = data.get("age")
    event = data.get("event")
    address = data.get("address")
    contact = data.get("contact")
    caption = f"Ma'lumotlarizngiz\n\n" \
              f"<b>FIO</b> {full_name}\n" \
              f"<b>Passport</b> {passport}\n" \
              f"<b>Yosh</b> {age}\n" \
              f"<b>Tanlov</b> {event}\n" \
              f"<b>Yashash joyi</b> {address}\n" \
              f"<b>Telefon Raqami</b> {contact}"
    print(caption)


@dp.message_handler(text = "👤 Ro'yxatdan o'tish")
async def start_register(message: types.Message):
    await message.answer(f"<b>Assalomu alaykum! {message.from_user.full_name}\n</b>"
                         "Ro'yxatdan o'tish uchun Ism Familiya Sharifingizni kiriting\n"
                         "Na'muna: <i> Abdullayev Abdulla Abdullayevich </i>", reply_markup=types.ReplyKeyboardRemove())
    await RegisterStates.full_name.set()

@dp.message_handler(state=RegisterStates.full_name)
async def get_full_name(message: types.Message, state:FSMContext):
    full_name = message.text
    await state.update_data(data={"full_name": full_name})
    await message.answer("<b>Passport seriyasi va raqamini birgalikda kiriting</b>\n\n "
                         "<i>Na'muna: AB1234567</i>", reply_markup=cancel_markup)
    await RegisterStates.next()

@dp.message_handler(state=RegisterStates.passport)
async def get_full_name(message: types.Message, state:FSMContext):
    passport = message.text
    if len(passport) == 9 and passport[:2].isalpha() and passport[2:].isdigit():
        await state.update_data(data={"passport": passport})
        await message.answer("<b>Yoshingizni raqamlarda kiriting - bu sizning tanlovdagi ishtirokingiz uchun muhim</b>\n"
                             "<i>Na'muna: 18</i>")
        await RegisterStates.next()
    else:
        await message.answer("Iltimos Passport raqamingizni to'g'ri kiriting")


@dp.message_handler(state=RegisterStates.age)
async def get_full_name(message: types.Message, state:FSMContext):
    age = int(message.text)
    if 18 <= age <= 100:
        await state.update_data(data={"age": age})
        await message.answer("<b>Qatnashmoqchi bo'lgan tanlovingizni belgilang</b>")
        await message.answer("Oldin, tanlovlar bilan to'liq tanishib chiqing\n\n"
                             "<b>* Eslatma: Tanlovlarning faqat bittasida ishtirok etish mumkin!</b>",
                             reply_markup=the_registerator_button)
        await RegisterStates.next()
    else:
        await message.answer("Sizning yoshingiz 18+ bolishi kerak")


@dp.callback_query_handler(state=RegisterStates.event)
async def get_event(call: types.CallbackQuery, state: FSMContext):
    event = call.data
    await state.update_data({"event": event})
    await call.message.delete()
    mark_up = types.ReplyKeyboardMarkup(resize_keyboard=True)
    mark_up.add(types.KeyboardButton(text = "📍 Joylashuvni yuborish", request_location=True))
    mark_up.add(types.KeyboardButton(text="❎ Bekor Qilish"))
    await call.message.answer("Tug'ildan joyingizni yoki hozirgi yashash joyingizni kiriting", reply_markup=mark_up)
    await RegisterStates.next()


@dp.message_handler(state=RegisterStates.address)
@dp.message_handler(content_types=["location"], state=RegisterStates.address)
async def get_address(message: types.Message, state:FSMContext):
    if message.location:
        lat = message.location.latitude
        long = message.location.longitude
        geolocator = Nominatim(user_agent="bot_location")
        location = geolocator.reverse(f"{lat}, {long}")
        address = location.address
    else:
        address = message.text
    await  state.update_data(data={"address": address})
    await message.answer("shahxsiy fotosuratingizni 3x4 formatda jonating", reply_markup=cancel_markup)
    await RegisterStates.next()

@dp.message_handler(state=RegisterStates.photo, content_types=["photo"])
async def get_photo(message: types.Message, state:FSMContext):
        photo = message.photo[-1].file_id
        await state.update_data({"photo_id": photo})
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton(text="Telefon raqamni Jo'natish", request_contact=True))
        markup.add(types.KeyboardButton(text="❎ Bekor Qilish"))
        await message.answer("Telefon Raqamingizni Yuboring", reply_markup=markup)
        await RegisterStates.next()

@dp.message_handler(state=RegisterStates.phone_number, content_types=["contact"])
async def get_photo(message: types.Message, state:FSMContext):
    contact = message.contact.phone_number
    await state.update_data({"contact": contact})
    await RegisterStates.next()
    data = await state.get_data()
    full_name = data.get("full_name")
    passport = data.get("passport")
    age = data.get("age")
    event = data.get("event")
    address = data.get("address")
    photo_id = data.get("photo_id")
    contact = data.get("contact")
    caption = f"Ma'lumotlarizngiz\n\n" \
              f"<b>FIO</b> {full_name}\n"\
              f"<b>Passport</b> {passport}\n"\
              f"<b>Yosh</b> {age}\n"\
              f"<b>Tanlov</b> {event}\n"\
              f"<b>Yashash joyi</b> {address}\n"\
              f"<b>Telefon Raqami</b> {contact}"
    choice = types.ReplyKeyboardMarkup(resize_keyboard=True)
    choice.add(types.KeyboardButton(text="✅ Qabul Qilish"))
    choice.add(types.KeyboardButton(text="❎ Bekor Qilish"))
    await message.answer_photo(photo=photo_id, caption=caption)
    await message.answer(text="Tepadagi habarlar to'grimi?", reply_markup=choice)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)